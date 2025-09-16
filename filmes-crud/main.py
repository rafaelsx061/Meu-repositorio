import sqlite3
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.metrics import dp

# Mantive exatamente como você tinha: DB = "filmes.db" mas uso o arquivo que você criou "meusfilmes.db"
DB = "filmes.db"

Window.clearcolor = (0.9, 0.2, 0.4, 1)

# Conexão e criação de tabela idêntica ao seu código
con = sqlite3.connect("meusfilmes.db")
cur = con.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INT NOT NULL
            )
    """)
con.commit()


# ---------- Tela de Cadastro (preserva seu código e nomes) ----------
class CadastroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Mantive seus TextInput exatamente (mesmos nomes)
        self.titulo_input = TextInput(
            hint_text="Digite o titulo do filme:",
            multiline=False,
            size_hint=(1, 0.15)
        )

        self.genero_input = TextInput(
            hint_text="Digite o genero do filme",
            size_hint=(1, 0.15)
        )

        self.ano_input = TextInput(
            hint_text='Ano',
            input_filter='int',
            size_hint=(1, 0.12)
        )

        salvar_btn = Button(
            text="Salvar",
            size_hint=(1, 0.12)
        )
        salvar_btn.bind(on_release=self.salvar_filme)

        botao_limpar = Button(
            text="Limpe suas escolhas",
            size_hint=(1, 0.12)
        )
        botao_limpar.bind(on_press=self.limpar)

        layout.add_widget(self.titulo_input)
        layout.add_widget(self.genero_input)
        layout.add_widget(self.ano_input)
        layout.add_widget(salvar_btn)
        layout.add_widget(botao_limpar)

        # Label simples para mensagens (preservando comportamento de prints também)
        self.msg_label = Label(text="", size_hint=(1, 0.08), color=(0, 0, 0, 1))
        layout.add_widget(self.msg_label)

        # botão para ir à lista
        ir_lista = Button(text="Ir para Lista", size_hint=(1, 0.12))
        ir_lista.bind(on_release=lambda inst: setattr(self.manager, 'current', 'listagem'))
        layout.add_widget(ir_lista)

        self.add_widget(layout)

    # Sua função salva praticamente inalterada (apenas atualiza label e lista)
    def salvar_filme(self, instance):
        titulo = self.titulo_input.text.strip()
        genero = self.genero_input.text.strip()
        ano = self.ano_input.text.strip()

        if titulo and genero and ano:  # Verifica se os campos não estão vazios
            try:
                cur.execute("INSERT INTO filmes (titulo, genero, ano) VALUES (?, ?, ?)",
                            (titulo, genero, ano))
                con.commit()
                self.titulo_input.text = ""
                self.genero_input.text = ""
                self.ano_input.text = ""
                self.msg_label.text = "Filme salvo com sucesso!"
                print("Filme salvo com sucesso!")
                # atualiza a lista se a tela existir
                if self.manager and 'listagem' in self.manager.screen_names:
                    self.manager.get_screen('listagem').listar_filmes()
            except Exception as e:
                self.msg_label.text = f"Erro ao salvar: {e}"
                print("Erro ao salvar:", e)
        else:
            self.msg_label.text = "Preencha todos os campos!"
            print("Preencha todos os campos!")

    def limpar(self, instance):
        # corrigi a limpeza para limpar os TextInput (mantendo nomes)
        self.titulo_input.text = ""
        self.genero_input.text = ""
        self.ano_input.text = ""
        self.msg_label.text = ""

    # wrapper com o nome pedido (mantive para compatibilidade)
    def adicionar_filme(self):
        self.salvar_filme(None)


# ---------- Tela de Listagem (nova) ----------
class ListagemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=12, spacing=8)

        # topo: busca + ordenar + voltar para cadastro
        topo = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        self.busca_input = TextInput(hint_text='Buscar por título (opcional)', multiline=False)
        self.busca_input.bind(text=lambda inst, val: self.listar_filmes())

        self.ordenar_spinner = Spinner(text='Nenhum', values=['Nenhum', 'Título', 'Ano'],
                                       size_hint_x=None, width=dp(120))
        self.ordenar_spinner.bind(text=lambda inst, val: self.listar_filmes())

        voltar_btn = Button(text='Novo Filme', size_hint_x=None, width=dp(100))
        voltar_btn.bind(on_release=lambda inst: setattr(self.manager, 'current', 'cadastro'))

        topo.add_widget(self.busca_input)
        topo.add_widget(self.ordenar_spinner)
        topo.add_widget(voltar_btn)
        root.add_widget(topo)

        # área de listagem (ScrollView com BoxLayout vertical)
        self.scroll = ScrollView(size_hint=(1, 1))
        self.lista_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=6, padding=6)
        self.lista_box.bind(minimum_height=self.lista_box.setter('height'))
        self.scroll.add_widget(self.lista_box)
        root.add_widget(self.scroll)

        self.add_widget(root)

    def on_pre_enter(self):
        self.listar_filmes()

    def listar_filmes(self):
        filtro = self.busca_input.text.strip()
        ordenar = self.ordenar_spinner.text

        query = "SELECT id, titulo, genero, ano FROM filmes"
        params = []
        if filtro:
            query += " WHERE titulo LIKE ?"
            params.append(f"%{filtro}%")
        if ordenar == 'Título':
            query += " ORDER BY titulo COLLATE NOCASE"
        elif ordenar == 'Ano':
            query += " ORDER BY ano"

        cur.execute(query, params)
        rows = cur.fetchall()

        # limpa lista atual
        self.lista_box.clear_widgets()

        for r in rows:
            fid, titulo, genero, ano = r
            linha = BoxLayout(size_hint_y=None, height=dp(48), padding=6, spacing=6)
            lbl = Label(text=f"{titulo} ({ano}) - {genero}", halign='left', valign='middle')
            lbl.text_size = (None, None)
            btn_edit = Button(text='Editar', size_hint_x=None, width=dp(80))
            btn_delete = Button(text='Excluir', size_hint_x=None, width=dp(80))

            # binds com captura do id
            btn_edit.bind(on_release=lambda inst, fid=fid: self._abrir_edicao(fid))
            btn_delete.bind(on_release=lambda inst, fid=fid: self._confirm_delete(fid))

            linha.add_widget(lbl)
            linha.add_widget(btn_edit)
            linha.add_widget(btn_delete)
            self.lista_box.add_widget(linha)

    def _abrir_edicao(self, filme_id):
        cur.execute("SELECT titulo, genero, ano FROM filmes WHERE id=?", (filme_id,))
        row = cur.fetchone()
        if not row:
            return
        titulo_val, genero_val, ano_val = row

        content = BoxLayout(orientation='vertical', spacing=8, padding=8)
        titulo_e = TextInput(text=str(titulo_val), multiline=False)
        genero_e = TextInput(text=str(genero_val), multiline=False)
        ano_e = TextInput(text=str(ano_val), multiline=False, input_filter='int')

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        salvar = Button(text='Salvar')
        cancelar = Button(text='Cancelar')
        btns.add_widget(salvar)
        btns.add_widget(cancelar)

        content.add_widget(Label(text='Editar Filme', size_hint_y=None, height=dp(30)))
        content.add_widget(titulo_e)
        content.add_widget(genero_e)
        content.add_widget(ano_e)
        content.add_widget(btns)

        popup = Popup(title='Editar', content=content, size_hint=(0.9, 0.6))

        def salvar_cb(instance):
            novo_t = titulo_e.text.strip()
            novo_g = genero_e.text.strip()
            novo_a = ano_e.text.strip()
            if not (novo_t and novo_g and novo_a):
                # feedback simples
                titulo_e.hint_text = "Preencha todos os campos!"
                return
            try:
                cur.execute("UPDATE filmes SET titulo=?, genero=?, ano=? WHERE id=?",
                            (novo_t, novo_g, novo_a, filme_id))
                con.commit()
                popup.dismiss()
                self.listar_filmes()
            except Exception as e:
                titulo_e.text = f"Erro: {e}"

        salvar.bind(on_release=salvar_cb)
        cancelar.bind(on_release=lambda inst: popup.dismiss())
        popup.open()

    def _confirm_delete(self, filme_id):
        content = BoxLayout(orientation='vertical', spacing=8, padding=8)
        content.add_widget(Label(text='Confirma exclusão deste filme?'))
        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        sim = Button(text='Sim')
        nao = Button(text='Não')
        btns.add_widget(sim)
        btns.add_widget(nao)
        content.add_widget(btns)
        popup = Popup(title='Confirmar excluir', content=content, size_hint=(0.7, 0.3))

        def confirmar(inst):
            try:
                cur.execute("DELETE FROM filmes WHERE id=?", (filme_id,))
                con.commit()
                popup.dismiss()
                self.listar_filmes()
            except Exception:
                popup.dismiss()

        sim.bind(on_release=confirmar)
        nao.bind(on_release=lambda inst: popup.dismiss())
        popup.open()

    # nomes pedidos pelo enunciado, implementados
    def editar_filme(self, filme_id, titulo, genero, ano):
        cur.execute("UPDATE filmes SET titulo=?, genero=?, ano=? WHERE id=?",
                    (titulo, genero, ano, filme_id))
        con.commit()
        self.listar_filmes()

    def deletar_filme(self, filme_id):
        cur.execute("DELETE FROM filmes WHERE id=?", (filme_id,))
        con.commit()
        self.listar_filmes()


# ---------- App com apenas duas telas: cadastro e lista ----------
class FilmesApp(App):
    def build(self):
        sm = ScreenManager()
        cadastro = CadastroScreen(name='cadastro')
        listagem = ListagemScreen(name='listagem')
        sm.add_widget(cadastro)
        sm.add_widget(listagem)
        sm.current = 'cadastro'  # inicia na sua tela original
        return sm


if __name__ == "__main__":
    FilmesApp().run()
