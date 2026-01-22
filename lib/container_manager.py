"""Manažer pro správu kontejnerů"""

from typing import Dict, Tuple, Any
from lib.config_manager import ConfigManager
from lib.udocker_wrapper import UDockerWrapper

class ContainerManager:
    def __init__(self, config_manager: ConfigManager, udocker: UDockerWrapper):
        self.config = config_manager
        self.udocker = udocker
    
    def get_all_containers_info(self) -> Dict[str, Dict[str, Any]]:
        """Získá informace o všech kontejnerech - spravovaných i externích"""
        config_containers = self.config.get_all_containers()
        if config_containers is None:
            config_containers = {}
        
        # Získat běžící kontejnery s kompletními detaily z inspect
        running_containers = self.udocker.get_running_containers()
        
        # Vytvořit mapu název -> container info pro rychlé vyhledávání
        running_by_name = {c['name']: c for c in running_containers}
        running_by_id = {c['id']: c for c in running_containers}
        
        all_containers = {}
        
        # Přidat spravované kontejnery z konfigurace
        for container_id, config in config_containers.items():
            container_name = config.get('name', container_id)
            
            # Zkontrolovat, zda běží podle názvu nebo ID
            running_info = running_by_name.get(container_name) or running_by_id.get(container_id)
            is_running = running_info is not None
            
            # Pokud běží, aktualizovat informace z inspect
            if is_running and running_info:
                # Mergovat konfiguraci s aktuálními informacemi z inspect
                all_containers[container_id] = {
                    **config,
                    'id': running_info.get('id', container_id),  # Použít skutečné ID z běžícího kontejneru
                    'name': container_name,  # Zachovat název z konfigurace
                    'running': True,
                    'managed': True,
                    # Aktualizovat z běžícího stavu (může se změnit)
                    'image': running_info.get('image', config.get('image', 'unknown')),
                }
            else:
                all_containers[container_id] = {
                    **config,
                    'id': container_id,
                    'name': container_name,
                    'running': False,
                    'managed': True
                }
        
        # Přidat externí (nespravované) běžící kontejnery
        for container_info in running_containers:
            container_name = container_info['name']
            container_id = container_info['id']
            
            # Zkontrolovat, zda už není v config pod názvem nebo ID
            already_managed = False
            for cfg_id, cfg in config_containers.items():
                if cfg.get('name') == container_name or cfg_id == container_id or cfg_id == container_name:
                    already_managed = True
                    break
            
            if not already_managed:
                # Použít informace z inspect, které už máme z get_running_containers
                all_containers[container_name] = {
                    'id': container_id,
                    'name': container_name,
                    'running': True,
                    'managed': False,
                    'autostart': False,
                    'image': container_info.get('image', 'unknown'),
                    'ports': container_info.get('ports', []),
                    'volumes': container_info.get('volumes', []),
                    'env': container_info.get('env', []),
                    'command': container_info.get('command', '')
                }
        
        return all_containers
    
    def create_and_start_container(self, container_config: Dict[str, Any]) -> Tuple[bool, str, str]:
        """Vytvoří kontejner, stáhne image pokud neexistuje, a spustí ho"""
        name = container_config['name']
        image = container_config['image']
        
        # Kontrola, zda image existuje
        if not self.udocker.image_exists(image):
            print(f"Image {image} neexistuje, stahuji...")
            success, message = self.udocker.pull_image(image)
            if not success:
                return False, f"Nelze stáhnout image: {message}", ""
        
        # Vytvoření kontejneru
        success, message = self.udocker.create_container(name, image)
        
        if not success:
            return False, message, ""
        
        # Uložení konfigurace
        self.config.save_container_config(name, container_config)
        
        # Automatické spuštění
        success, start_message = self.start_container(name)
        
        if success:
            return True, f"Kontejner {name} vytvořen a spuštěn", name
        else:
            return True, f"Kontejner {name} vytvořen, ale nepodařilo se spustit: {start_message}", name
    
    def update_container(self, container_id: str, new_config: Dict[str, Any]) -> Tuple[bool, str]:
        """Aktualizuje kontejner - smaže starý a vytvoří nový s novou konfigurací"""
        # Zkusit zastavit a smazat starý kontejner (může už neexistovat)
        try:
            stop_success, stop_msg = self.udocker.stop_container(container_id)
            # Ignorujeme chybu - kontejner možná už neexistuje
        except Exception as e:
            print(f"Upozornění při mazání starého kontejneru: {e}")
        
        # Smazat starou konfiguraci
        self.config.delete_container_config(container_id)
        
        # Vytvořit a spustit nový kontejner s novou konfigurací
        success, message, new_id = self.create_and_start_container(new_config)
        
        if success:
            return True, f"Kontejner aktualizován: {message}"
        else:
            return False, f"Chyba při vytváření nového kontejneru: {message}"
    
    def start_container(self, container_id: str) -> Tuple[bool, str]:
        """Spustí kontejner s konfigurací"""
        container_config = self.config.get_container_config(container_id)
        
        # Pokud kontejner neexistuje, musíme ho nejdřív vytvořit
        all_containers = self.udocker.get_all_containers()
        container_exists = any(c['id'] == container_id or c['name'] == container_id for c in all_containers)
        
        if not container_exists:
            # Kontejner neexistuje, vytvoříme ho
            image = container_config.get('image', 'unknown')
            if image == 'unknown':
                return False, "Nelze spustit kontejner bez image"
            
            # Zkontrolovat, zda image existuje
            if not self.udocker.image_exists(image):
                success, message = self.udocker.pull_image(image)
                if not success:
                    return False, f"Nelze stáhnout image: {message}"
            
            # Vytvořit kontejner
            success, message = self.udocker.create_container(container_id, image)
            if not success:
                return False, f"Nelze vytvořit kontejner: {message}"
        
        # Nyní spustit kontejner
        return self.udocker.run_container(
            container_id,
            volumes=container_config.get('volumes', []),
            ports=container_config.get('ports', []),
            env=container_config.get('env', []),
            command=container_config.get('command')
        )
    
    def stop_container(self, container_id: str) -> Tuple[bool, str]:
        """Zastaví kontejner"""
        return self.udocker.stop_container(container_id)
    
    def delete_container(self, container_id: str) -> Tuple[bool, str]:
        """Smaže kontejner"""
        # Nejdřív zkusit zastavit (smazat běžící kontejner)
        try:
            self.udocker.stop_container(container_id)
        except Exception:
            pass  # Může být už zastavený nebo neexistovat
        
        # Smazat z udockeru
        success, message = self.udocker.delete_container(container_id)
        
        # Smazat konfiguraci (i když smazání z udockeru selhalo)
        self.config.delete_container_config(container_id)
        
        if success:
            return True, f"Kontejner {container_id} smazán"
        else:
            # I když selhalo mazání, config jsme smazali
            return True, f"Kontejner odstraněn z konfigurace"
    
    def save_running_container(self, container_id: str) -> Tuple[bool, str]:
        """Uloží běžící externí kontejner do konfigurace"""
        # Získat informace o kontejneru pomocí inspect
        inspect_info = self.udocker.inspect_container(container_id)
        
        container_config = {
            'name': inspect_info.get('name', container_id),
            'image': inspect_info.get('image', 'unknown'),
            'autostart': False,
            'ports': inspect_info.get('ports', []),
            'volumes': inspect_info.get('volumes', []),
            'env': inspect_info.get('env', []),
            'command': inspect_info.get('command', '')
        }
        
        self.config.save_container_config(container_id, container_config)
        return True, f"Kontejner {container_id} uložen do konfigurace"
    
    def sync_running_containers(self):
        """Synchronizuje běžící kontejnery s konfigurací"""
        running = self.udocker.get_running_containers()
        config_containers = self.config.get_all_containers()
        
        for container in running:
            if container['id'] not in config_containers:
                print(f"  • Nalezen externí kontejner: {container['id']}")
    
    def autostart_all(self) -> Dict[str, Tuple[bool, str]]:
        """Spustí všechny kontejnery s nastaveným autostartem"""
        results = {}
        containers = self.config.get_all_containers()
        if containers is None:
            return results
        
        for container_id, config in containers.items():
            if config.get('autostart'):
                success, message = self.start_container(container_id)
                results[config['name']] = (success, message)
        
        return results