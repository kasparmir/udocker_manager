"""Wrapper pro práci s udocker příkazy"""

import subprocess
import json
import re
from typing import List, Dict, Tuple, Any

class UDockerWrapper:
    def __init__(self):
        self.udocker_cmd = 'udocker'
    
    def run_command(self, args: List[str], timeout: int = 30) -> Dict[str, Any]:
        """Spustí udocker příkaz a vrátí výsledek"""
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
        """Zkontroluje, zda je udocker nainstalován"""
        return self.run_command(['version'])['success']
    
    def get_running_containers(self) -> List[Dict[str, str]]:
        """Získá seznam běžících kontejnerů s jejich názvy a detaily"""
        result = self.run_command(['ps'])
        containers = []
        
        if result['success'] and result['stdout']:
            lines = result['stdout'].strip().split('\n')
            
            # Zpracovat řádky s kontejnery
            for line in lines:
                if not line.strip() or 'CONTAINER ID' in line.upper():
                    continue
                    
                parts = line.split()
                if not parts or len(parts) < 2:
                    continue
                
                container_id = parts[0]
                
                # Extrahovat název z hranatých závorek
                # Formát: ['název']
                name_match = re.search(r"\['([^']+)'\]", line)
                if name_match:
                    container_name = name_match.group(1)
                else:
                    # Pokud není v závorkách, použít ID
                    container_name = container_id
                
                # Získat detaily pomocí inspect
                inspect_info = self.inspect_container(container_name)
                
                containers.append({
                    'id': container_id,
                    'name': container_name,
                    'running': True,
                    'image': inspect_info.get('image', 'unknown'),
                    'ports': inspect_info.get('ports', []),
                    'volumes': inspect_info.get('volumes', []),
                    'env': inspect_info.get('env', []),
                    'command': inspect_info.get('command', '')
                })
        
        return containers
    
    def get_all_containers(self) -> List[Dict[str, str]]:
        """Získá seznam všech kontejnerů (běžících i zastavených)"""
        result = self.run_command(['ps', '-a'])
        containers = []
        
        if result['success'] and result['stdout']:
            for line in result['stdout'].strip().split('\n'):
                if not line.strip() or 'CONTAINER' in line.upper():
                    continue
                
                parts = line.split()
                if not parts:
                    continue
                
                container_id = parts[0]
                
                # Extrahovat název z hranatých závorek
                name_match = re.search(r"\['([^']+)'\]", line)
                if name_match:
                    container_name = name_match.group(1)
                else:
                    container_name = container_id
                
                containers.append({
                    'id': container_id,
                    'name': container_name
                })
        
        return containers
    
    def inspect_container(self, container_name: str) -> Dict[str, Any]:
        """Získá detailní informace o kontejneru pomocí udocker inspect"""
        result = self.run_command(['inspect', container_name])
        
        info = {
            'name': container_name,
            'image': 'unknown',
            'ports': [],
            'volumes': [],
            'env': [],
            'command': ''
        }
        
        if not result['success'] or not result['stdout']:
            print(f"Inspect selhal pro {container_name}: {result.get('stderr', 'no output')}")
            return info
        
        try:
            # Parsovat JSON výstup
            data = json.loads(result['stdout'])
            
            print(f"\n=== Inspect výstup pro {container_name} ===")
            
            # Získat informace z config sekce
            config = data.get('config', {})
            
            # Command
            cmd = config.get('Cmd', [])
            if cmd:
                info['command'] = ' '.join(cmd) if isinstance(cmd, list) else str(cmd)
                print(f"  Command: {info['command']}")
            
            # Environment variables
            env_list = config.get('Env', [])
            for env_var in env_list:
                if '=' in env_var:
                    var_name = env_var.split('=')[0]
                    # Odfiltruj systémové proměnné
                    if var_name not in ['PATH', 'HOME', 'USER', 'SHELL', 'PWD', 'OLDPWD', 
                                       'ROCKET_PROFILE', 'ROCKET_ADDRESS', 'ROCKET_PORT', 
                                       'DEBIAN_FRONTEND']:
                        info['env'].append(env_var)
                        print(f"  ENV: {env_var}")
            
            # Exposed ports
            exposed_ports = config.get('ExposedPorts', {})
            for port_key in exposed_ports.keys():
                # Formát: "80/tcp" nebo "8080/udp"
                port_num = port_key.split('/')[0]
                # Pro exposed porty použijeme stejný port na hostu i v kontejneru
                port_str = f"{port_num}:{port_num}"
                if port_str not in info['ports']:
                    info['ports'].append(port_str)
                    print(f"  Port (exposed): {port_str}")
            
            # Volumes
            volumes = config.get('Volumes', {})
            for volume_path in volumes.keys():
                # Default volume mount - použijeme stejnou cestu
                vol_str = f"{volume_path}:{volume_path}"
                if vol_str not in info['volumes']:
                    info['volumes'].append(vol_str)
                    print(f"  Volume: {vol_str}")
            
            # Zkusit získat image info
            # Možnost 1: Ze source label
            labels = config.get('Labels', {})
            image_source = labels.get('org.opencontainers.image.source', '')
            image_version = labels.get('org.opencontainers.image.version', '')
            
            if image_source and image_version:
                # Zkusit extrahovat repo name
                repo_match = re.search(r'github\.com/([^/]+/[^/]+)', image_source)
                if repo_match:
                    repo_name = repo_match.group(1).replace('/', '_')
                    info['image'] = f"{repo_name}:{image_version}"
                    print(f"  Image (from labels): {info['image']}")
            
            # Možnost 2: Zkusit udocker ps pro získání image
            if info['image'] == 'unknown':
                ps_result = self.run_command(['ps'])
                if ps_result['success']:
                    for line in ps_result['stdout'].split('\n'):
                        if container_name in line:
                            # Hledat IMAGE sloupec
                            parts = line.split()
                            # Format: CONTAINER_ID P M ['NAME'] IMAGE
                            if len(parts) >= 5:
                                # IMAGE je obvykle na indexu 4 nebo 5
                                for i in range(3, len(parts)):
                                    if '/' in parts[i] or ':' in parts[i]:
                                        info['image'] = parts[i]
                                        print(f"  Image (from ps): {info['image']}")
                                        break
                            break
            
            print(f"=== Konec inspect pro {container_name} ===\n")
        
        except json.JSONDecodeError as e:
            print(f"Chyba při parsování JSON pro {container_name}: {e}")
            print(f"Výstup: {result['stdout'][:200]}")
        except Exception as e:
            print(f"Chyba při zpracování inspect výstupu pro {container_name}: {e}")
            import traceback
            traceback.print_exc()
        
        return info
    
    def get_images(self) -> List[Dict[str, str]]:
        """Získá seznam lokálních images"""
        result = self.run_command(['images'])
        images = []
        
        if result['success'] and result['stdout']:
            for line in result['stdout'].strip().split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        repo = parts[0]
                        tag = parts[1] if len(parts) > 1 else 'latest'
                        
                        # Sestavit celé jméno
                        full_name = f"{repo}:{tag}"
                        
                        # Odstranit trailing dvojtečku pokud existuje
                        full_name = full_name.rstrip(':')
                        
                        images.append({
                            'repository': repo,
                            'tag': tag,
                            'full_name': full_name
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
        """Vytvoří nový kontejner"""
        result = self.run_command(['create', f'--name={name}', image])
        if result['success']:
            return True, f"Kontejner {name} vytvořen"
        return False, result['stderr'] or "Chyba při vytváření"
    
    def run_container(self, container_id: str, volumes: List[str] = None,
                     ports: List[str] = None, env: List[str] = None,
                     command: str = None) -> Tuple[bool, str]:
        """Spustí kontejner s parametry na pozadí"""
        import subprocess
        import os
        
        args = [self.udocker_cmd, 'run']
        
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
            args.extend(command.split())
        
        try:
            # Spustit proces na pozadí pomocí subprocess.Popen
            # Oddělit od terminálu a přesměrovat výstup
            process = subprocess.Popen(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,  # Oddělí proces od terminálu
                cwd=os.path.expanduser('~')
            )
            
            # Počkat krátkou chvíli na kontrolu, zda proces nezhavaroval hned
            import time
            time.sleep(1)
            
            # Zkontrolovat, zda proces stále běží
            poll = process.poll()
            if poll is not None and poll != 0:
                return False, f"Kontejner se nepodařilo spustit (exit code: {poll})"
            
            return True, f"Kontejner {container_id} spuštěn na pozadí"
            
        except Exception as e:
            return False, f"Chyba při spouštění: {str(e)}"
    
    def stop_container(self, container_id: str) -> Tuple[bool, str]:
        """Zastaví a smaže běžící kontejner"""
        # udocker nemá příkaz 'stop', použijeme 'rm' pro smazání
        result = self.run_command(['rm', container_id])
        if result['success']:
            return True, f"Kontejner {container_id} zastaven a smazán"
        return False, result['stderr'] or "Chyba při zastavování"
    
    def delete_container(self, container_id: str) -> Tuple[bool, str]:
        """Smaže kontejner"""
        result = self.run_command(['rm', container_id])
        if result['success']:
            return True, f"Kontejner {container_id} smazán"
        return False, result['stderr'] or "Chyba při mazání"
    
    def pull_image(self, image: str) -> Tuple[bool, str]:
        """Stáhne image z registru"""
        result = self.run_command(['pull', image], timeout=600)
        if result['success']:
            return True, f"Image {image} stažen"
        return False, result['stderr'] or "Chyba při stahování"
    
    def delete_image(self, image: str) -> Tuple[bool, str]:
        """Smaže lokální image"""
        result = self.run_command(['rmi', image])
        if result['success']:
            return True, f"Image {image} smazán"
        return False, result['stderr'] or "Chyba při mazání"
    
    def prune_unused_images(self) -> Tuple[bool, str]:
        """Smaže nepoužívané images"""
        # Získat všechny images
        images = self.get_images()
        
        # Získat všechny kontejnery
        all_containers = self.get_all_containers()
        
        # Získat používané images z běžících kontejnerů
        used_images = set()
        for container in all_containers:
            container_name = container.get('name', container.get('id'))
            inspect_info = self.inspect_container(container_name)
            if inspect_info and inspect_info.get('image') != 'unknown':
                used_images.add(inspect_info['image'])
        
        # Smazat nepoužívané images
        deleted = 0
        deleted_names = []
        
        for image in images:
            image_name = image['full_name']
            
            # Zkontrolovat různé varianty názvu
            is_used = False
            for used in used_images:
                if (image_name == used or 
                    image_name in used or 
                    used in image_name or
                    image['repository'] in used):
                    is_used = True
                    break
            
            if not is_used:
                success, msg = self.delete_image(image_name)
                if success:
                    deleted += 1
                    deleted_names.append(image_name)
        
        if deleted > 0:
            return True, f"Smazáno {deleted} nepoužívaných images: {', '.join(deleted_names[:3])}{'...' if len(deleted_names) > 3 else ''}"
        else:
            return True, "Žádné nepoužívané images k smazání"