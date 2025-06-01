import os
import sys
import tty
import json
import random
import shutil
import termios
import platform
import subprocess
from colorama import Fore, Style

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def Load_BD():
    with open("Scripts_Itunes/Script.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def Load_Config():
     with open("Scripts_Itunes/User/config.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)
     
def Acceso_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def AutoRUN():
    if '--fondo' in sys.argv:
        idx = sys.argv.index('--fondo')
        video = sys.argv[idx + 1]
        mensaje = None
        if '--mensaje' in sys.argv:
            idx2 = sys.argv.index('--mensaje')
            mensaje = sys.argv[idx2 + 1]
        if mensaje:
            print(f"\n🛠️  {mensaje}\n")
        subprocess.run(["xwinwrap", "-ov", "-fs", "--", "mpv", "--loop", "--no-audio", "--wid=WID", video])
        sys.exit()
    
def Carpeta_Fondos_Creador(modo):
    dato = Load_BD()
    data = Load_Config()

    if modo == "Funcion1":
        Rut = dato["Rutas"][1]
        existe = "FondoDePantallaIMG"
    elif modo == "Funcion2":
        Rut = dato["Rutas"][0]
        existe = "FondoDePantallaVideo"

    if data[existe][0] == "false":
        partes = Rut.strip("/").split("/")
        ruta_actual = ""
        for carpeta in partes:
            ruta_actual = os.path.join(ruta_actual, carpeta)
            if not os.path.exists(ruta_actual):
                os.mkdir(ruta_actual)
    
    if modo == "Funcion1":
        Validador("FondoDePantallaIMG", "true")
    elif modo == "Funcion2":
        Validador("FondoDePantallaVideo", "true")

def Guardar_IMGMP4(modo, ruta):
    dato = Load_BD()
    Carpeta_Fondos_Creador(modo)

    if modo == "Funcion1":
        Rut = dato["Rutas"][1]
    elif modo == "Funcion2":
        Rut = dato["Rutas"][0]

    nombre = os.path.basename(ruta)
    ruta_destino = os.path.join(Rut, nombre)
    shutil.copy2(ruta, ruta_destino)

    if modo == "Funcion2":
        return ruta_destino
    
def autoinicio_itunes(ruta_video_local):
    dato = Load_BD()
    contenido = dato["Autostart"]
    mensaje="Arranque automático del fondo animado"

    autostart_dir = os.path.expanduser("~/.config/autostart")
    if not os.path.exists(autostart_dir):
        os.makedirs(autostart_dir)

    ruta_programa = os.path.abspath(__file__)
    comando = f"python3 {ruta_programa} --fondo '{ruta_video_local}'"
    
    if mensaje:
        comando += f" --mensaje \"{mensaje}\""

    contenido = contenido.replace("{{comando}}", comando)
    with open(os.path.join(autostart_dir, "itunes_fondo.desktop"), "w") as f:
        f.write(contenido)

def Validador(clave, valor):
    ruta = "Scripts_Itunes/User/config.json"
    data = Load_Config()

    if clave in data:
        data[clave][0] = valor
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def logo():
    dato = Load_BD()
    icon = dato["Logo"][0]
    data = dato["Version"][1]
    clear()
    print(Fore.CYAN + icon.encode().decode("unicode_escape") + Fore.RESET)
    print (Style.BRIGHT + "    " + data + " - by NesAnTime " + Style.RESET_ALL)

def Fondos_Funcion1():
    logo()
    print(f"\n  ⚠️   {Fore.YELLOW + Style.DIM}Seleccionaste la opción de cambiar el fondo de pantalla.{Fore.RESET}")
    print(f"  🔗   Por favor, proporciona la ruta del archivo de imagen que deseas establecer como fondo de pantalla.{Style.RESET_ALL}")
    ruta = input("\n   📲   Ruta de la imagen: ").strip()
    ruta = ruta.strip("'").strip('"')

    while not os.path.isfile(ruta):
        print(f"   ⚠️   {Fore.RED}La ruta proporcionada no es válida. Asegúrate de que el archivo exista.{Fore.RESET}")
        ruta = input("\n   📲   Ruta de la imagen: ").strip()
        ruta = ruta.strip("'").strip('"')
        
    while not ruta.lower().endswith(('.png', '.jpg')):
        print(f"   ⚠️   {Fore.RED}El archivo debe ser una imagen válida (png, jpg).{Fore.RESET}")
        ruta = input("\n   📲   Ruta de la imagen: ").strip()
        ruta = ruta.strip("'").strip('"')

    Guardar_IMGMP4(modo="Funcion1", ruta=ruta)
    print(f"\n  ⚙️   {Style.BRIGHT}Estableciendo el fondo de pantalla...{Style.RESET_ALL}")

    subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-path", "-s", ruta])
    print(f"\n  ✅   {Fore.GREEN + Style.BRIGHT}Fondo de pantalla establecido correctamente.{Fore.RESET}")



def Fondos_Funcion2():
    dato = Load_BD()
    data = Load_Config()
    logo()

    print(f"\n  ⚠️   {Fore.YELLOW + Style.DIM}Seleccionaste la opción de cambiar el fondo de pantalla a fondo Animado.{Fore.RESET}\n")
    if data["FondoDePantallaVideo"][0] == "false":
        print(f"  ⚠️   {Fore.YELLOW + Style.NORMAL}NOTA: {Fore.RESET} Esta Funcion no es nativa de XFCE (Kali Linux), por lo que es necesario añadir a {Style.BRIGHT}ItunesCuztomizer{Style.NORMAL} a la lista de aplicaciones de arranque para aplicar el fondo animado en cada inicio de sesión.")
        print(f"  ⚠️   {Fore.YELLOW + Style.DIM}Asegúrate de que el video sea compatible con el formato MP4.{Fore.RESET}\n")

        
        print(f"  📋   {Style.RESET_ALL}Presiona Enter o Espacio para aceptar y continuar... (ESC/BORRAR/SUPR para salir)")
        while True:
            Tecla = Acceso_key()
            if Tecla in ['\x1b', '\x08', '\x7f']:
                print(f"\n   ❌   {Fore.RED + Style.DIM}No se Puede Continuar Permisos Denegados, Programa finalizado por el usuario.{Fore.RESET + Style.RESET_ALL}")
                sys.exit()
            elif Tecla in ['\r', ' ']:
                print(f"\n   ✅   {Fore.GREEN + Style.BRIGHT}Permisos Aceptados, Continuando...{Fore.RESET + Style.RESET_ALL}")
                break
    else:
        print(f"  🔗   {Fore.YELLOW + Style.DIM}Por favor, proporciona la ruta del video que deseas establecer como fondo de pantalla animado.{Style.RESET_ALL}")
    
    ruta = input("\n   📲   Ruta del video (.mp4):").strip()
    ruta = ruta.strip("'").strip('"')

    while not os.path.isfile(ruta):
        print(f"   ⚠️   {Fore.RED}La ruta proporcionada no es válida. Asegúrate de que el archivo exista.{Fore.RESET}")
        ruta = input("\n   📲   Ruta del video (.mp4):").strip()
        ruta = ruta.strip("'").strip('"')
        
    while not ruta.lower().endswith(('.mp4')):
        print(f"   ⚠️   {Fore.RED}El archivo debe ser una imagen válida (png, jpg).{Fore.RESET}")
        ruta = input("\n   📲   Ruta del video (.mp4):").strip()
        ruta = ruta.strip("'").strip('"')

    info_ruta = Guardar_IMGMP4(modo="Funcion2", ruta=ruta)
    autoinicio_itunes(info_ruta, mensaje="Arranque automático del fondo animado")

    subprocess.run(["xwinwrap", "-ov", "-fs", "--", "mpv", "--loop", "--no-audio", "--wid=WID", info_ruta])
    print(f"\n  ✅   {Fore.GREEN + Style.BRIGHT}Fondo de pantalla animado establecido correctamente.{Fore.RESET}")





def main():
    AutoRUN()
    dato = Load_BD()
    frase = dato["RamdomFrases"][random.randint(0, 5)]
    logo()
    print(f"\n 🗣️  {Style.DIM + frase + Style.RESET_ALL}\n")

    print(f"➖➖➖➖➖  Menu de opciones  ➖➖➖➖➖")
    print("    1️⃣   Fondo de Pantalla (Wallpaper)")
    print("    2️⃣   Fondo de Pantalla (Animado)")

    while True:
        opc = input(f"\n {Fore.YELLOW}[!]{Fore.RESET} Selecciona una opcion: ")
        if opc == "1":
            Fondos_Funcion1()
            break
        elif opc == "2":
            Fondos_Funcion2()
            break
        else:
            print(f"⚠️   {Fore.RED}Opción no válida, por favor intenta de nuevo.{Fore.RESET}")


main()
