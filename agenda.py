from tkinter import *
import sqlite3

		
class Banco:
	'''
	Cria banco de dados e as propriedades conn e cursor
	
	Funções e seus parâmetros de entrada:
		- inserir_novo: nome, telefone, email
		- atualizar_lista: nenhum
		- excluir: id
		- exibir: id
		- excluir: id
	'''
	
	def __init__(self):
		self.conn = sqlite3.connect("agenda.db")
		self.cursor = self.conn.cursor()
		
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS contatos (
				id integer primary key,
				nome text not null,
				telefone text not null,
				email text not null
			)
		""")
		self.conn.commit()
		
	def inserir_novo(self, nome, telefone, email):
		self.cursor.execute(f"INSERT INTO contatos (nome, telefone, email) VALUES ('{nome}','{telefone}','{email}')")
		self.conn.commit()
		
	def atualizar_lista(self):
		contatos = self.cursor.execute("SELECT * FROM contatos")
		return contatos
		
	def excluir(self, index):
		self.cursor.execute(f"DELETE FROM contatos WHERE id = {index}")
		self.conn.commit()		
		
	def exibir(self, index):
		contato = self.cursor.execute(f"SELECT * FROM contatos WHERE id = {index}")
		return contato
		
	def editar(self, index, nome, telefone, email):
		self.cursor.execute(f"UPDATE contatos SET nome = '{nome}', telefone = '{telefone}', email = '{email}' WHERE id = {index}")
		self.conn.commit()		
		

class Agenda:
	'''
	Cria uma interface gráfica com os elementos necessários para 
	a amnipulação de dados de contatos contendo nome, telefone e email.
	
	Funções e seus parâmetros:
		- resetar: nenhum
		- atualizar: nenhum
		- adicionar: nenhum
		- excluir: nenhum
		- editar: nenhum
		- confirmar_edicao: nenhum
		- mensagem: msg
	'''
	def __init__(self, master):
		self.master = master
		
		self.fonte_padrao = "Courier 10 bold"
		self.bg_frm1 = "#333333"
		self.fg_frm1 = "#ffffff"		
		self.bg_btn = "#FE642E"
		
		self.frame_1 = Frame(self.master)
		self.frame_1.configure(background = self.bg_frm1)
		self.frame_1.place(x = 30, y = 30, w = 640, h = 180)
		
		self.lbl_nome = Label(self.frame_1, text = "Nome: ", bg = self.bg_frm1, fg = self.fg_frm1, font = self.fonte_padrao).place(x = 20, y = 10)
		self.lbl_telefone = Label(self.frame_1, text = "Tel.: ", bg = self.bg_frm1, fg = self.fg_frm1, font = self.fonte_padrao).place(x = 20, y = 50)
		self.lbl_email = Label(self.frame_1, text = "E-mail: ", bg = self.bg_frm1, fg = self.fg_frm1, font = self.fonte_padrao).place(x = 20, y = 90)
		
		self.ipt_nome = Entry(self.frame_1, font = self.fonte_padrao)
		self.ipt_nome.place(x = 80, y = 10, w = 540)
		
		self.ipt_telefone = Entry(self.frame_1, font = self.fonte_padrao)
		self.ipt_telefone.place(x = 80, y = 50, w = 540)
		
		self.ipt_email = Entry(self.frame_1, font = self.fonte_padrao)
		self.ipt_email.place(x = 80, y = 90, w = 540)
		
		self.btn_resetar = Button(self.frame_1, text = "Limpar", command=self.resetar, bg = self.bg_btn, height = 1, font = self.fonte_padrao)
		self.btn_resetar.place(x = 95, y = 130, w = 140)
		
		self.btn_adicionar = Button(self.frame_1, text = "Adicionar", command=self.adicionar, bg = self.bg_btn, height = 1, font = self.fonte_padrao)
		self.btn_adicionar.place(x = 415, y = 130, w = 140)
		
		self.scrollbar = Scrollbar(self.master)
		self.scrollbar.place(x = 670, y = 240, w = 15, h = 200)
		
		self.lbx_contatos = Listbox(self.master, font="Courier 10", yscrollcommand = self.scrollbar.set, selectbackground = "#2E9AFE", height = 12)
		self.lbx_contatos.place(x = 30, y = 240, w = 640)
		
		self.btn_editar = Button(self.master, text = "Editar", command = self.editar, bg = self.bg_btn, height = 1, font = self.fonte_padrao)
		self.btn_editar.place(x = 110, y = 460, w = 140)
		
		self.btn_excluir = Button(self.master, text = "Deletar", command=self.excluir, bg = self.bg_btn, height = 1, font = self.fonte_padrao)
		self.btn_excluir.place(x = 460, y = 460, w = 140)
		
		self.editar_index = ""
		self.editar_nome = ""
		self.editar_telefone = ""
		self.editar_email = ""
		self.editar_janela = ""
		
		self.atualizar()
		
	def resetar(self):
		'''
		Função acionada pelo clique no batao 'btn_resetar'.Limpa os 
		valores inseridos nos inputs e troca o background para branco 
		e foca novamente no input do nome.
		'''
		self.ipt_nome.delete(0, "end")
		self.ipt_telefone.delete(0, "end")
		self.ipt_email.delete(0, "end")						
		
		self.ipt_nome["bg"] = "#FFFFFF"
		self.ipt_telefone["bg"] = "#FFFFFF"
		self.ipt_email["bg"] = "#FFFFFF"
		
		self.ipt_nome.focus()
		
	def atualizar(self):
		'''
		Limpa a listagem de contatos para que ela possa ser atualizada
		corretamente. Usa o retorno da função 'atualizar_lista'
		do banco de dados. É acionada toda vez que o programe é aberto,
		quando algum contato é adicionado, alterado ou removido.
		'''
		self.lbx_contatos.delete(0, "end")
		
		contatos = Banco().atualizar_lista()
		for c in contatos.fetchall():
			contato = f"{c[0]:<3} - {c[1][:25]:<28} - {c[2]:<13} - {c[3]}"
			self.lbx_contatos.insert(0, contato)
					
				
	def adicionar(self):
		'''
		Função acionada pelo clique no botao 'btn_adicionar'. Lê os
		valores dos inputs e verifica se eles possuem tamanho líquido de
		espaços maiores do que zero. Altera o background daqueles inputs
		que não atendam a essa condição. Caso contrário, usa os valores
		dos inputs como parâmetros para a função 'inserir_novo' do banco
		de dados.
		'''
		nome = self.ipt_nome.get()
		telefone = self.ipt_telefone.get()
		email = self.ipt_email.get()
		
		if len(nome.split()) > 0 and len(telefone.split()) > 0 and len(email.split()) > 0:						
			Banco().inserir_novo(nome, telefone, email)					
			self.resetar()
			self.atualizar()
			
			self.mensagem("Contato adicionado com sucesso!")
			
		else:
			if len(nome.split()) == 0:
				self.ipt_nome["bg"] = "#F5A9A9"
			else:
				self.ipt_nome["bg"] = "#FFFFFF"
			if len(telefone.split()) == 0:
				self.ipt_telefone["bg"] = "#F5A9A9"
			else:
				self.ipt_telefone["bg"] = "#FFFFFF"
			if len(email.split()) == 0:
				self.ipt_email["bg"] = "#F5A9A9"
			else:
				self.ipt_email["bg"] = "#FFFFFF"									
		
	def excluir(self):
		'''
		Função acionada pelo clique no botao 'btn_excluir'. Recupera o
		valor da linha selecionada na 'lbx_contatos' e o usa como 
		parâmetro na função 'excluir' do banco de dados.
		'''
		index = self.lbx_contatos.curselection()[0]
		selecionado = self.lbx_contatos.get(index).split()[0]
		
		Banco().excluir(int(selecionado))
		
		self.atualizar()
		
		self.mensagem("Contato excluido com sucesso!")
		
		
	def editar(self):
		'''
		Função acionada pelo clique no botao 'btn_editar'. Recupera o 
		valor da linha da 'lbx_contatos' como indice para a função
		'exibir' do banco de dados, para que os dados sejam carregados
		na janela pop-up que se abrirá.
		
		O botao 'btn' possui o comando 'confirmar_edicao' que recupera
		os valores dos inputs da 'editar_janela' e os usa no funcao
		'editar' do banco de dados.
	
		'''
		index = self.lbx_contatos.curselection()[0]
		selecionado = self.lbx_contatos.get(index).split()[0]
		
		contato = list(Banco().exibir(int(selecionado)))
		
		self.editar_janela = Tk()
		
		lbl_nome = Label(self.editar_janela, text = "Nome: ").place(x = 20, y = 10)
		lbl_telefone = Label(self.editar_janela, text = "Tel.: ").place(x = 20, y = 50)
		lbl_email = Label(self.editar_janela, text = "E-mail: ").place(x = 20, y = 90)
		
		self.editar_index = contato[0][0]
		
		self.editar_nome = Entry(self.editar_janela)
		self.editar_nome.insert(0, contato[0][1])
		self.editar_nome.place(x = 80, y = 10, w = 340)
		
		self.editar_telefone = Entry(self.editar_janela)
		self.editar_telefone.insert(0, contato[0][2])
		self.editar_telefone.place(x = 80, y = 50, w = 340)
		
		self.editar_email = Entry(self.editar_janela)
		self.editar_email.insert(0, contato[0][3])
		self.editar_email.place(x = 80, y = 90, w = 340)
				
		btn = Button(self.editar_janela, text="Confirmar alterações", command = self.confirma_edicao)
		btn.place(x = 150, y = 130, w = 150)
		
		self.editar_janela.geometry("450x180+112+90")
		self.editar_janela.title("Editar contato")
		self.editar_janela.mainloop()
		
	def confirma_edicao(self):	
		'''
		Usa os valores do inputs da 'editar_janela' para atualizar o 
		contato usando a funcao 'editar' do banco de dados'
		
		AINDA NÃO TEM NENHUMA VELIDAÇÃO DE DADOS.
		'''	
		nome = self.editar_nome.get()
		telefone = self.editar_telefone.get()
		email = self.editar_email.get()
		
		Banco().editar(int(self.editar_index), nome, telefone, email)		
		
		self.editar_janela.destroy()
		self.atualizar()
		
		self.editar_index = ""
		self.editar_nome = ""
		self.editar_telefone = ""
		self.editar_email = ""
		self.editar_janela = ""
		
		self.mensagem("Contato atualizado com sucesso!")
		
	def mensagem(self, msg):
		'''
		Cria uma janela pop-up que exibe uma mensagem passada como
		parâmetro.
		'''
		janela = Tk()
		janela.title("Agenda")
		janela.geometry("300x100+200+150")
		
		m = Label(janela, text = msg).place(x = 0, y = 20, w = 300)
		b = Button(janela, text = "Fechar", command = janela.destroy)
		b.place(x = 100, y = 60, w = 100)
		
		
		
		
		
		
root = Tk()
Agenda(root)
root.geometry("700x500+0+0")
root.title("Agenda - NoobPythonBR")
root.mainloop()
