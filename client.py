import socket, time, pickle, matplotlib.pyplot as plt, sched

scheduler = sched.scheduler(time.time, time.sleep)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((socket.gethostname(), 9999))

def print_sched(lista):
    print("Uso do RAM:")
    for i in range(10):
        print(f' {lista[i]} Mb')
        time.sleep(0.3)
    print('-' *40, '\n')
    print("Uso do cpu:")
    for i in range(10,len(lista)):
        print(f'{lista[i]} %')
        time.sleep(0.3)

def grafico(lista):
    data_RAM = []
    data_CPU = []
    for i in range(10):
        data_RAM.append(lista[i])
    for i in range(10,len(lista)):
        data_CPU.append(lista[i])
    fig, axs = plt.subplots(2)
    axs[0].plot(data_RAM)
    axs[1].set_ylabel("Em %")
    axs[0].set_title("Monitoramento do RAM e CPU(respectivamente)")
    axs[1].set_ylim([0,100])
    axs[1].plot(data_CPU)
    axs[0].set_ylabel("Em Mb")
    plt.show()

def print_list(l,msg):   
    print("="*40)        
    if msg == 'ram':
        print(f'Capacidade máxima de memória: {l[0]}')
        print(f'memória disponível: {l[1]}')
    elif msg == 'ramcpu':
        scheduler.enter(priority=1, delay=1, action=print_sched, argument=(l,))
        scheduler.enter(priority=2, delay=8, action=grafico, argument=(l,))
        scheduler.run()
    elif msg == 'cpu':
        print(f'Nome :{l[0]} \nFrequencia máxima: {l[1]} Hz \nFrequência em uso {l[2]} Hz \nNúmero de nucleos físicos: {l[3]}')
        print(f'Número de nucloes lógicos: {l[4]} \npalavra do processador: {l[5]}')
    elif msg == 'proc':
        for i in l:
            print(f'{i}')
            time.sleep(0.3)
    elif msg == 'net':
        time.sleep(1.5)
        print(f'IP: {l[0]}  Máscara: {l[1]} Getway: {l[2]}')  
        print("-"*40,"\nInformações nmap:")
        for i in range(3,len(l),4):
            print(f"Host: {l[i]} || Protocolo: {l[i+1]} || Port: {l[i+2]} || status: {l[i+3]}")
            time.sleep(0.5)
    elif msg == 'path':
        for i in range(0,len(l),4):
            print(f'Nome: {l[i]} || Tamanho: {l[i+1]} Mb || Data de Criação: {l[i+2]} || Data de Modificação: {l[i+3]}')
    print("="*40)

def show_options():
    print(" cpu - Uso da CPU\n",
    "ram - Memoria RAM usada\n",
    "proc - Nome dos processos em execução\n",
    "net - Informacoes de rede\n",
    "path - para ver arquivos\n",
    "ramcpu - para ver o uso de ram e do cpu em gráfico\n",
    "fim - encerrar conexão")
    print(" ")
    choice = str(input("Entre com a opaçao desejada: "))
    return choice

msg = show_options()
try:
    while msg != 'fim':
        s.send(msg.encode('ascii'))
        if msg != 'fim':
            info_bytes = s.recv(1000000)
            lista = pickle.loads(info_bytes)
            print_list(lista,msg)
            time.sleep(2)
            msg = show_options()
except Exception as erro:
    print(str(erro))
s.send(msg.encode('ascii'))
s.close()