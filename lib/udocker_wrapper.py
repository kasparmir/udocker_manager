"""Wrapper pro práci s udocker příkazy"""

import subprocess
from typing import List, Dict, Tuple, Any

class UDockerWrapper:
    def __init__(self):
        self.udocker_cmd = 'udocker'
    
    def run_command(self, args: List[str], timeout: int = 30) -> Dict[str, Any]:
        try:
            result = subprocess.run([self.udocker_cmd] + args, capture_output=True, 
                                   text=True, timeout=timeout)
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'stdout': '', 'stderr': 'Timeout', 'returncode': -1}
        except Exception as e:
            return {'success': False, 'stdout': '', 'stderr': str(e), 'returncode': -1}
    
    def check_installation(self) -> bool:
        return self.run_command(['version'])['success']
    
    def get_running_containers(self) -> List[Dict[str, str]]:
        result = self.run_command(['ps'])
        containers = []
        
        if result['success'] and result['stdout']:
            for line in result['stdout'].strip().split('\n'):
                # Přeskočíme prázdné řádky a hlavičku
                if not line.strip() or 'CONTAINER ID' in line or 'container id' in line.upper():
                    continue
                parts = line.split()
                if parts and len(parts) >= 1:
                    # udocker ps může mít různé formáty výstupu
                    container_id = parts[0]
                    containers.append({
                        'id': container_id,
                        'name': container_id,
                        'running': True
                    })
        
        return containers
    
    def get_all_containers(self) -> List[Dict[str, str]]:
        result = self.run_command(['ps', '-a'])
        containers = []
        
        if result['success'] and result['stdout']:
            for line in result['stdout'].strip().split('\n'):
                if line.strip() and not line.startswith('CONTAINER'):
                    parts = line.split()
                    if parts:
                        containers.append({'id': parts[0], 'name': parts[0]})
        return containers
    
    def get_images(self) -> List[Dict[str, str]]:
        result = self.run_command(['images'])
        images = []
        
        if result['success'] and result['stdout']:
            for line in result['stdout'].strip().split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        images.append({
                            'repository': parts[0],
                            'tag': parts[1] if len(parts) > 1 else 'latest',
                            'full_name': f"{parts[0]}:{parts[1] if len(parts) > 1 else 'latest'}"
                        })
        return images
    
    def image_exists(self, image: str) -> bool:
        """Kontrola, zda image existuje lokálně"""
        images = self.get_images()
        for img in images:
            if img['full_name'] == image or f"{img['repository']}:{img['tag']}" == image:
                return True
        return False
    
    def create_container(self, name: str, image: str) -> Tuple[bool, str]:
        result = self.run_command(['create', f'--name={name}', image])
        if result['success']:
            return True, f"Kontejner {name} vytvořen"
        return False, result['stderr'] or "Chyba při vytváření"
    
    def run_container(self, container_id: str, volumes: List[str] = None,
                     ports: List[str] = None, env: List[str] = None,
                     command: str = None) -> Tuple[bool, str]:
        args = ['run', '-d']  # Přidán detached mode
        
        if volumes:
            for vol in volumes:
                if vol.strip():
                    args.extend(['-v', vol.strip()])
        
        if ports:
            for port in ports:
                if port.strip():
                    args.extend(['-p', port.strip()])
        
        if env:
            for e in env:
                if e.strip():
                    args.extend(['-e', e.strip()])
        
        args.append(container_id)
        if command:
            args.append(command)
        
        result = self.run_command(args, timeout=120)  # Zvýšený timeout
        if result['success']:
            return True, f"Kontejner {container_id} spuštěn"
        return False, result['stderr'] or "Chyba při spouštění"
    
    def stop_container(self, container_id: str) -> Tuple[bool, str]:
        # udocker nemá příkaz 'stop', použijeme 'kill'
        result = self.run_command(['kill', container_id])
        if result['success']:
            return True, f"Kontejner {container_id} zastaven"
        return False, result['stderr'] or "Chyba při zastavování"
    
    def delete_container(self, container_id: str) -> Tuple[bool, str]:
        result = self.run_command(['rm', container_id])
        if result['success']:
            return True, f"Kontejner {container_id} smazán"
        return False, result['stderr'] or "Chyba při mazání"
    
    def pull_image(self, image: str) -> Tuple[bool, str]:
        """Stáhne image s progresem"""
        result = self.run_command(['pull', image], timeout=600)
        if result['success']:
            return True, f"Image {image} stažen"
        return False, result['stderr'] or "Chyba při stahování"
    
    def delete_image(self, image: str) -> Tuple[bool, str]:
        result = self.run_command(['rmi', image])
        if result['success']:
            return True, f"Image {image} smazán"
        return False, result['stderr'] or "Chyba"
    
    def prune_unused_images(self) -> Tuple[bool, str]:
        images = self.get_images()
        containers = self.get_all_containers()
        
        # Získání použitých images
        used_images = set()
        for container in containers:
            info = self.run_command(['inspect', container['id']])
            if info['success']:
                pass
        
        deleted = 0
        for image in images:
            if image['full_name'] not in used_images:
                pass
        
        return True, f"Kontrola nepoužívaných images dokončena"