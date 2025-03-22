import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QClipboard
from senha_repositorio import SenhaRepositorio

ARQUIVO_SENHAS = "senhas_seguradas.dat"
SALT = b'segredo-sal-fixo'

class GerenciadorSenhas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySecret - Gerenciador de Senhas")
        self.setMinimumSize(600, 450)

        self.lista_senhas = QListWidget()
        self.lista_senhas.itemDoubleClicked.connect(self.mostrar_senha)

        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar...")
        self.campo_busca.textChanged.connect(self.filtrar_senhas)

        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_remover = QPushButton("Remover")
        self.botao_editar = QPushButton("Editar")
        self.botao_copiar_usuario = QPushButton("Copiar Usuário")
        self.botao_copiar_senha = QPushButton("Copiar Senha")

        self.botao_adicionar.clicked.connect(self.adicionar_senha)
        self.botao_remover.clicked.connect(self.remover_senha)
        self.botao_editar.clicked.connect(self.editar_senha)
        self.botao_copiar_usuario.clicked.connect(self.copiar_usuario)
        self.botao_copiar_senha.clicked.connect(self.copiar_senha)

        layout_botoes = QHBoxLayout()
        for botao in [self.botao_adicionar, self.botao_editar, self.botao_remover, 
                      self.botao_copiar_usuario, self.botao_copiar_senha]:
            layout_botoes.addWidget(botao)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Senhas salvas:"))
        layout.addWidget(self.campo_busca)
        layout.addWidget(self.lista_senhas)
        layout.addLayout(layout_botoes)
        self.setLayout(layout)

        self.solicitar_senha_mestra()

    def solicitar_senha_mestra(self):
        senha, ok = QInputDialog.getText(self, "Senha Mestra", "Digite sua senha mestra:", QLineEdit.EchoMode.Password)
        if ok and senha:
            self.repositorio = SenhaRepositorio(ARQUIVO_SENHAS, senha, SALT)
            self.carregar_senhas()
        else:
            QMessageBox.critical(self, "Erro", "Senha mestra é obrigatória.")
            self.close()

    def carregar_senhas(self):
        self.dados_senhas = self.repositorio.carregar()
        self.atualizar_lista_senhas()

    def atualizar_lista_senhas(self):
        self.lista_senhas.clear()
        for item in self.dados_senhas:
            self.lista_senhas.addItem(f"{item['servico']} | {item['usuario']}")

    def salvar_senhas(self):
        self.repositorio.salvar(self.dados_senhas)

    def adicionar_senha(self):
        servico, ok1 = QInputDialog.getText(self, "Serviço", "Nome do serviço:")
        if not ok1 or not servico: return
        usuario, ok2 = QInputDialog.getText(self, "Usuário", "Nome de usuário:")
        if not ok2 or not usuario: return
        senha, ok3 = QInputDialog.getText(self, "Senha", "Senha:", QLineEdit.EchoMode.Password)
        if not ok3 or not senha: return
        self.dados_senhas.append({"servico": servico, "usuario": usuario, "senha": senha})
        self.salvar_senhas()
        self.atualizar_lista_senhas()

    def remover_senha(self):
        idx = self.lista_senhas.currentRow()
        if idx >= 0:
            del self.dados_senhas[idx]
            self.salvar_senhas()
            self.atualizar_lista_senhas()

    def editar_senha(self):
        idx = self.lista_senhas.currentRow()
        if idx >= 0:
            item = self.dados_senhas[idx]
            servico, ok1 = QInputDialog.getText(self, "Editar Serviço", "Serviço:", text=item['servico'])
            if not ok1: return
            usuario, ok2 = QInputDialog.getText(self, "Editar Usuário", "Usuário:", text=item['usuario'])
            if not ok2: return
            senha, ok3 = QInputDialog.getText(self, "Editar Senha", "Senha:", QLineEdit.EchoMode.Password, text=item['senha'])
            if not ok3: return
            self.dados_senhas[idx] = {"servico": servico, "usuario": usuario, "senha": senha}
            self.salvar_senhas()
            self.atualizar_lista_senhas()

    def mostrar_senha(self, item):
        idx = self.lista_senhas.row(item)
        senha = self.dados_senhas[idx]['senha']
        QMessageBox.information(self, "Senha", f"Senha: {senha}")

    def copiar_usuario(self):
        idx = self.lista_senhas.currentRow()
        if idx >= 0:
            usuario = self.dados_senhas[idx]['usuario']
            QApplication.clipboard().setText(usuario)

    def copiar_senha(self):
        idx = self.lista_senhas.currentRow()
        if idx >= 0:
            senha = self.dados_senhas[idx]['senha']
            QApplication.clipboard().setText(senha)

    def filtrar_senhas(self):
        termo = self.campo_busca.text().lower()
        for i in range(self.lista_senhas.count()):
            item = self.lista_senhas.item(i)
            item.setHidden(termo not in item.text().lower())

def aplicar_estilo_completo(app):
    # Paleta Escura
    paleta = QPalette()
    paleta.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
    paleta.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    paleta.setColor(QPalette.ColorRole.Base, QColor("#353535"))
    paleta.setColor(QPalette.ColorRole.AlternateBase, QColor("#404040"))
    paleta.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    paleta.setColor(QPalette.ColorRole.Button, QColor("#3c3c3c"))
    paleta.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    paleta.setColor(QPalette.ColorRole.Highlight, QColor("#007bff"))
    paleta.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    app.setPalette(paleta)

    # CSS extra para detalhes
    estilo = """
    QPushButton {
        border-radius: 5px;
        padding: 6px 12px;
        background-color: #4a4a4a;
        color: white;
    }
    QPushButton:hover {
        background-color: #5a5a5a;
    }
    QPushButton:pressed {
        background-color: #333333;
    }
    QListWidget, QLineEdit {
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 5px;
        background-color: #353535;
    }
    QLabel {
        font-weight: 600;
    }
    """
    app.setStyleSheet(estilo)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    aplicar_estilo_completo(app)
    janela = GerenciadorSenhas()
    janela.show()
    sys.exit(app.exec())