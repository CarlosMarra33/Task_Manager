import socket, psutil, pickle, os, platform, netifaces, cpuinfo
from datetime import datetime

def cpu_info():
    data_cpu = []
    info = cpuinfo.get_cpu_info()
    data_cpu.append(platform.processor()) 
    data_cpu.append(psutil.cpu_freq().max)
    data_cpu.append(psutil.cpu_freq().current)
    data_cpu.append(psutil.cpu_count(logical=False))
    data_cpu.append(psutil.cpu_count())
    data_cpu.append(info['bits'])
    return data_cpu

def ram_info():
    data_ram = []
    total = psutil.virtual_memory().total/(1024*1024*1024)
    disponivel = psutil.virtual_memory().available/(1024*1024*1024)
    data_ram.append(round(total,2))
    data_ram.append(round(disponivel,2))
    return data_ram

def proc_info():
    data_proc = []
    for i in psutil.pids():
        if psutil.pid_exists(i):
            p = psutil.Process(i)
            with p.oneshot():
                data_proc.append(f'pid:{p.ppid()} || nome: {p.name()} || consumo de CPU: {p.cpu_percent()} || uso de RAM: {p.memory_info().rss}')
    return data_proc[:10]

def net_info():
    data_net = []
    gateway = netifaces.gateways()
    net_info = psutil.net_if_addrs()
    for i in net_info["Ethernet"]:
        if str(i.family) == 'AddressFamily.AF_INET':
            data_net.append(i.address)
            data_net.append(i.netmask)
            data_net.append(gateway['default'][2][0]) 
                
    file_txt = open("nmap_data.txt", "r")
    txt_data = file_txt.read()
    for i in txt_data.split("\n"):
        data_net.append(i)
    return data_net

def path_info():
    path = 'C:\\Users\\Carlos\\Documents'
    data_path = []
    lista =  os.listdir(path)
    for i in lista:
        data_path.append(i)
        data_path.append(str(round(os.stat(f'{path}\{i}').st_size / 1024 ** 2 ,2)))
        data_path.append(str(datetime.fromtimestamp(int(os.stat(f'{path}\{i}').st_ctime))))
        data_path.append(datetime.fromtimestamp(int(os.stat(f'{path}\{i}').st_mtime)))
    return data_path

def ramcpu_info():
    data_ramcpu = []
    for i in range(10):
        mem = psutil.virtual_memory().used//1024 ** 2
        data_ramcpu.append(round(mem,2))
    for i in range(10):
        data_ramcpu.append(psutil.cpu_percent(interval=1))
    return data_ramcpu

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket_servidor.bind((socket.gethostname() , 9999))
socket_servidor.listen()
print("Servidor de nome", socket.gethostname(), "esperando conexão na porta", 9999)
(socket_cliente,addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

while True:
    
    msg = socket_cliente.recv(1024)
    if msg.decode('ascii') == 'cpu':
        socket_cliente.send(pickle.dumps(cpu_info()))    
    elif msg.decode('ascii') == 'ram':
        socket_cliente.send(pickle.dumps(ram_info())) 
    elif msg.decode('ascii') == 'proc':
        socket_cliente.send(pickle.dumps(proc_info()))    
    elif msg.decode('ascii') == 'net':
        socket_cliente.send(pickle.dumps(net_info()))  
    elif msg.decode('ascii') == 'path':
        socket_cliente.send(pickle.dumps(path_info()))
    elif msg.decode('ascii') == 'ramcpu':
        socket_cliente.send(pickle.dumps(ramcpu_info()))
    elif msg.decode('ascii') == 'fim':
        break

socket_cliente.close()
socket_servidor.close()