import tkinter as tk
from tkinter import messagebox, ttk
import datetime

# ===== Estilos =====
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 10, 'bold'), background='#4CAF50', foreground='white', padding=5)
style.map('TButton', background=[('active', '#45a049')])
style.configure('TLabel', font=('Arial', 10), background='#f0f8ff')
style.configure('TCheckbutton', font=('Arial', 9), background='#f0f8ff')
style.configure('TNotebook', background='#f0f8ff')
style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
style.configure('Treeview', font=('Arial', 9), rowheight=25)
style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background='#e0e0e0')

# ===== Dados globais =====
pacientes = []
fila = []
medicos = [
    {'nome': 'Dr. João Silva', 'especialidade': 'Clínico Geral', 'horario': '10:00-14:00'},
    {'nome': 'Dra. Maria Santos', 'especialidade': 'Clínico Geral', 'horario': '16:00-20:00'},
    {'nome': 'Dr. Pedro Oliveira', 'especialidade': 'Clínico Geral', 'horario': '20:00-24:00'}
]

# ===== Funções =====
def validar_cpf(cpf):
    cpf = cpf.replace('.', '').replace('-', '').strip()
    return len(cpf) == 11 and cpf.isdigit()

def atualizar_estatisticas():
    if not pacientes:
        text_estatisticas.delete(1.0, tk.END)
        text_estatisticas.insert(tk.END, "📊 Nenhum paciente cadastrado.")
        return
    total = len(pacientes)
    idades = [p['idade'] for p in pacientes]
    media_idade = sum(idades)/total
    mais_novo = min(pacientes, key=lambda p: p['idade'])
    mais_velho = max(pacientes, key=lambda p: p['idade'])
    msg = f"📈 Número total de pacientes: {total}\n"
    msg += f"📉 Idade média: {media_idade:.2f}\n"
    msg += f"👶 Paciente mais novo: {mais_novo['nome']} ({mais_novo['idade']} anos)\n"
    msg += f"👴 Paciente mais velho: {mais_velho['nome']} ({mais_velho['idade']} anos)"
    text_estatisticas.delete(1.0, tk.END)
    text_estatisticas.insert(tk.END, msg)

def cadastrar_paciente():
    nome = entry_nome.get().strip()
    idade_str = entry_idade.get().strip()
    telefone = entry_telefone.get().strip()
    cpf = entry_cpf.get().strip()
    try:
        if not nome or not telefone or not cpf:
            raise ValueError("Nome, telefone e CPF não podem ser vazios.")
        if not validar_cpf(cpf):
            raise ValueError("CPF deve ter exatamente 11 dígitos numéricos.")
        idade = int(idade_str)
        if idade < 0 or idade > 150:
            raise ValueError("Idade deve ser um número positivo e realista.")
        pacientes.append({'nome': nome, 'idade': idade, 'telefone': telefone, 'cpf': cpf})
        messagebox.showinfo("✅ Sucesso", "Paciente cadastrado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        atualizar_lista_pacientes()
        atualizar_estatisticas()
        atualizar_combobox_acesso()
        atualizar_combobox_fila()
    except ValueError as e:
        messagebox.showerror("❌ Erro", str(e))

def buscar_paciente():
    nome_busca = entry_busca.get().strip().lower()
    text_resultados.delete(1.0, tk.END)
    if nome_busca:
        encontrados = [p for p in pacientes if nome_busca in p['nome'].lower()]
        if encontrados:
            msg = "🔍 Resultados:\n" + "\n".join(
                [f"👤 Nome: {p['nome']}, Idade: {p['idade']}, Telefone: {p['telefone']}, CPF: {p['cpf']}" for p in encontrados])
            text_resultados.insert(tk.END, msg)
        else:
            text_resultados.insert(tk.END, "❌ Paciente não encontrado.")
    else:
        text_resultados.insert(tk.END, "Digite um nome para buscar.")

def atualizar_lista_pacientes():
    for row in tree.get_children():
        tree.delete(row)
    for p in pacientes:
        tree.insert("", tk.END, values=(p['nome'], p['idade'], p['telefone'], p['cpf']))

def atualizar_combobox_fila():
    combobox_fila['values'] = [p['nome'] for p in pacientes]
    if pacientes:
        combobox_fila.current(0)

def adicionar_paciente_fila():
    paciente_selecionado = combobox_fila.get()
    if not paciente_selecionado:
        messagebox.showerror("❌ Erro", "Selecione um paciente primeiro.")
        return
    paciente = next((p for p in pacientes if p['nome'] == paciente_selecionado), None)
    if paciente and paciente not in [item['paciente'] for item in fila]:
        numero_chamada = len(fila) + 1
        fila.append({'paciente': paciente, 'numero_chamada': numero_chamada})
        atualizar_lista_fila()
        messagebox.showinfo("✅ Sucesso", f"Paciente {paciente_selecionado} adicionado à fila (Chamada {numero_chamada}).")
    else:
        messagebox.showwarning("⚠️ Aviso", "Paciente já está na fila ou não encontrado.")

def atender_paciente_fila():
    if fila:
        atendido = fila.pop(0)
        messagebox.showinfo("🏥 Atendido", f"Paciente atendido: {atendido['paciente']['nome']} (CPF: {atendido['paciente']['cpf']}, Chamada {atendido['numero_chamada']})")
        atualizar_lista_fila()
    else:
        messagebox.showinfo("📭 Fila", "Fila vazia.")

def atualizar_lista_fila():
    listbox_fila.delete(0, tk.END)
    for item in fila:
        p = item['paciente']
        num = item['numero_chamada']
        listbox_fila.insert(tk.END, f"📞 Chamada {num}: {p['nome']} (CPF: {p['cpf']})")

def atualizar_combobox_acesso():
    combobox_acesso['values'] = [p['nome'] for p in pacientes]
    if pacientes:
        combobox_acesso.current(0)
        atualizar_checkboxes()

# ===== Controle de Acesso =====
def atualizar_cores():
    label_A.config(fg='green' if var_A.get() else 'red')
    label_B.config(fg='green' if var_B.get() else 'red')
    label_C.config(fg='green' if var_C.get() else 'red')
    label_D.config(fg='green' if var_D.get() else 'red')

def atualizar_checkboxes():
    paciente_selecionado = combobox_acesso.get()
    horario = entry_horario.get().strip()

    # A: paciente na fila
    var_A.set(any(item['paciente']['nome'] == paciente_selecionado for item in fila))

    # B: CPF válido
    paciente = next((p for p in pacientes if p['nome'] == paciente_selecionado), None)
    var_B.set(validar_cpf(paciente['cpf']) if paciente else False)

    # C: Médico disponível
    medico_ok = False
    try:
        hora_atual = datetime.datetime.strptime(horario, '%H:%M').time()
        for medico in medicos:
            inicio, fim = medico['horario'].split('-')
            hora_inicio = datetime.datetime.strptime(inicio, '%H:%M').time()
            hora_fim = datetime.datetime.strptime(fim, '%H:%M').time()
            if hora_inicio <= hora_atual <= hora_fim:
                medico_ok = True
                break
    except ValueError:
        medico_ok = False
    var_C.set(medico_ok)

    atualizar_cores()

def verificar_acesso():
    paciente_selecionado = combobox_acesso.get()
    horario_atual = entry_horario.get().strip()
    A = var_A.get()
    B = var_B.get()
    C = var_C.get()
    D = var_D.get()
    consulta_normal = (A and B and C) or (B and C and D)
    emergencia = C and (B or D)
    msg = f"👤 Paciente: {paciente_selecionado}\n🕒 Horário: {horario_atual}\n"
    msg += f"🔍 Condições: A={A}, B={B}, C={C}, D={D}\n\n"
    msg += f"📅 Consulta Normal: {'✅ Atendido' if consulta_normal else '❌ Não atendido'}\n"
    msg += f"🚑 Emergência: {'✅ Atendido' if emergencia else '❌ Não atendido'}"
    text_acesso.delete(1.0, tk.END)
    text_acesso.insert(tk.END, msg)

def limpar_verificacao():
    text_acesso.delete(1.0, tk.END)
    var_A.set(False)
    var_B.set(False)
    var_C.set(False)
    var_D.set(False)
    entry_horario.delete(0, tk.END)
    atualizar_cores()

# ===== Janela principal =====
root = tk.Tk()
root.title("🏥 Sistema Clínica Vida+")
root.geometry("1000x800")
root.configure(bg='#f0f8ff')

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- Aba Cadastro ---
frame_cadastro = ttk.Frame(notebook, padding=20)
notebook.add(frame_cadastro, text="📝 Cadastro")
ttk.Label(frame_cadastro, text="👤 Cadastre um Novo Paciente", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
ttk.Label(frame_cadastro, text="Nome:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_nome = ttk.Entry(frame_cadastro, width=30); entry_nome.grid(row=1, column=1, pady=5)
ttk.Label(frame_cadastro, text="Idade:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_idade = ttk.Entry(frame_cadastro, width=30); entry_idade.grid(row=2, column=1, pady=5)
ttk.Label(frame_cadastro, text="Telefone:").grid(row=3, column=0, sticky=tk.W, pady=5)
entry_telefone = ttk.Entry(frame_cadastro, width=30); entry_telefone.grid(row=3, column=1, pady=5)
ttk.Label(frame_cadastro, text="CPF (11 dígitos):").grid(row=4, column=0, sticky=tk.W, pady=5)
entry_cpf = ttk.Entry(frame_cadastro, width=30); entry_cpf.grid(row=4, column=1, pady=5)
ttk.Button(frame_cadastro, text="✅ Cadastrar Paciente", command=cadastrar_paciente).grid(row=5, column=0, columnspan=2, pady=20)

# --- Aba Estatísticas ---
frame_estatisticas = ttk.Frame(notebook, padding=20)
notebook.add(frame_estatisticas, text="📊 Estatísticas")
ttk.Label(frame_estatisticas, text="📈 Estatísticas da Clínica", font=('Arial', 12, 'bold')).pack(pady=10)
text_estatisticas = tk.Text(frame_estatisticas, height=10, width=70, font=('Arial', 10), bg='#ffffff', relief=tk.FLAT)
text_estatisticas.pack(pady=10)
ttk.Button(frame_estatisticas, text="🔄 Atualizar", command=atualizar_estatisticas).pack()

# --- Aba Buscar ---
frame_buscar = ttk.Frame(notebook, padding=20)
notebook.add(frame_buscar, text="🔍 Buscar")
ttk.Label(frame_buscar, text="🔍 Busque um Paciente", font=('Arial', 12, 'bold')).pack(pady=10)
ttk.Label(frame_buscar, text="Nome para buscar:").pack(pady=5)
entry_busca = ttk.Entry(frame_buscar, width=40); entry_busca.pack(pady=5)
ttk.Button(frame_buscar, text="🔍 Buscar", command=buscar_paciente).pack(pady=10)
text_resultados = tk.Text(frame_buscar, height=8, width=70, font=('Arial', 10), bg='#ffffff', relief=tk.FLAT)
text_resultados.pack(pady=10)

# --- Aba Listar ---
frame_listar = ttk.Frame(notebook, padding=20)
notebook.add(frame_listar, text="📋 Listar")
ttk.Label(frame_listar, text="📋 Pacientes Cadastrados", font=('Arial', 12, 'bold')).pack(pady=10)
tree = ttk.Treeview(frame_listar, columns=("Nome", "Idade", "Telefone", "CPF"), show="headings", height=10)
for col in ("Nome", "Idade", "Telefone", "CPF"):
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

# --- Aba Fila ---
frame_fila = ttk.Frame(notebook, padding=20)
notebook.add(frame_fila, text="⏳ Fila")
ttk.Label(frame_fila, text="⏳ Gerenciar Fila de Atendimento", font=('Arial', 12, 'bold')).pack(pady=10)
ttk.Label(frame_fila, text="Selecione um Paciente Cadastrado:").pack(pady=5)
combobox_fila = ttk.Combobox(frame_fila, state="readonly", width=40); combobox_fila.pack(pady=5)
ttk.Button(frame_fila, text="➕ Adicionar à Fila", command=adicionar_paciente_fila).pack(pady=10)
ttk.Button(frame_fila, text="🏥 Atender Primeiro", command=atender_paciente_fila).pack(pady=5)
ttk.Label(frame_fila, text="📭 Fila Atual:").pack(pady=10)
listbox_fila = tk.Listbox(frame_fila, height=10, font=('Arial', 10), bg='#ffffff', relief=tk.FLAT)
listbox_fila.pack(fill=tk.BOTH, expand=True)

# --- Aba Controle de Acesso ---
frame_acesso = ttk.Frame(notebook, padding=20)
notebook.add(frame_acesso, text="🔐 Controle de Acesso")
ttk.Label(frame_acesso, text="🔐 Verifique Acesso ao Atendimento", font=('Arial', 12, 'bold')).pack(pady=10)
ttk.Label(frame_acesso, text="👨‍⚕️ Médicos Disponíveis:", font=('Arial', 10, 'bold')).pack(pady=5)
for medico in medicos:
    ttk.Label(frame_acesso, text=f"{medico['nome']} ({medico['especialidade']}) - Horário: {medico['horario']}").pack(pady=2)
ttk.Label(frame_acesso, text="Selecione um Paciente:").pack(pady=5)
combobox_acesso = ttk.Combobox(frame_acesso, state="readonly", width=40)
combobox_acesso.pack(pady=5)
ttk.Label(frame_acesso, text="Horário (HH:MM):").pack(pady=5)
entry_horario = ttk.Entry(frame_acesso, width=20)
entry_horario.pack(pady=5)

# Checkboxes e labels coloridos
frame_condicoes = ttk.Frame(frame_acesso)
frame_condicoes.pack(pady=10)
label_A = tk.Label(frame_condicoes, text="A: Paciente na fila", font=('Arial', 10))
label_B = tk.Label(frame_condicoes, text="B: Documentos OK", font=('Arial', 10))
label_C = tk.Label(frame_condicoes, text="C: Médico disponível", font=('Arial', 10))
label_D = tk.Label(frame_condicoes, text="D: Pagamentos em dia", font=('Arial', 10))
label_A.grid(row=0, column=0, padx=10, sticky='w')
label_B.grid(row=0, column=1, padx=10, sticky='w')
label_C.grid(row=1, column=0, padx=10, sticky='w')
label_D.grid(row=1, column=1, padx=10, sticky='w')

var_A = tk.BooleanVar(); var_B = tk.BooleanVar(); var_C = tk.BooleanVar(); var_D = tk.BooleanVar()
check_A = tk.Checkbutton(frame_condicoes, variable=var_A, command=atualizar_cores)
check_B = tk.Checkbutton(frame_condicoes, variable=var_B, command=atualizar_cores)
check_C = tk.Checkbutton(frame_condicoes, variable=var_C, command=atualizar_cores)
check_D = tk.Checkbutton(frame_condicoes, variable=var_D, command=atualizar_cores)
check_A.grid(row=0, column=0, sticky='e')
check_B.grid(row=0, column=1, sticky='e')
check_C.grid(row=1, column=0, sticky='e')
check_D.grid(row=1, column=1, sticky='e')

ttk.Button(frame_acesso, text="🔍 Verificar Acesso", command=verificar_acesso).pack(pady=5)
ttk.Button(frame_acesso, text="🧹 Limpar", command=limpar_verificacao).pack(pady=5)
text_acesso = tk.Text(frame_acesso, height=8, width=70, font=('Arial', 10), bg='#ffffff', relief=tk.FLAT)
text_acesso.pack(pady=10)

# Atualiza checkboxes ao selecionar paciente ou horário
def evento_acesso(event=None):
    atualizar_checkboxes()
combobox_acesso.bind("<<ComboboxSelected>>", evento_acesso)
entry_horario.bind("<FocusOut>", evento_acesso)

root.mainloop()
