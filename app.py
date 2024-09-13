import PySimpleGUI as sg
from loteria_caixa import *


loterias = [
    "MegaSena",
    "LotoFacil",
    "Quina",
    "LotoMania",
    "TimeMania",
    "DuplaSena",
    "Federal",
    "Loteca",
    "DiadeSorte",
    "SuperSet",
]


# layout
def window():

    sg.theme("kayak")
    sg.TRANSPARENT_BUTTON = (sg.theme_background_color(), sg.theme_background_color())

    cel_0 = [
        [
            sg.Text("Nº do concurso:", font="serif 12"),
            sg.In(font="arial 11", key="-CONCURSO-", size=6, enable_events=True),
            sg.Text("Loteria:", font="serif 12"),
            sg.Combo(
                loterias, size=19, key="-LOTERIA-", readonly=True, enable_events=True
            ),
        ]
    ]

    cel_1 = [
        [sg.Text("Resultado do sorteio", text_color="purple", font="serif 12")],
        [
            sg.Multiline(
                "",
                key="-GABARITO-",
                text_color="blue",
                font="arial 12",
                size=(40, 2),
                no_scrollbar=True,
            )
        ],
    ]

    cel_2 = [
        [sg.Text("Aquivo com as apostas", font="serif 12")],
        [
            sg.In(key="-GAME-", text_color="blue", font="arial 11", size=41),
            sg.FileBrowse(size=5),
        ],
    ]

    coluna1 = [
        [sg.Frame("", layout=cel_0)],
        [
            sg.Frame(
                "", layout=cel_1, key="-CEL1-", visible=False, relief=sg.RELIEF_FLAT
            )
        ],
        [sg.Frame("", layout=cel_2)],
        [
            sg.Submit(
                font="serif 13 italic", size=(6, 1), button_color=("white", "green")
            )
        ],
    ]

    coluna2 = [
        [
            sg.B(
                "Help",
                button_color=sg.TRANSPARENT_BUTTON,
                image_size=(15, 15),
                image_filename="question-sign-circles_41943.png",
                image_subsample=2,
                border_width=0,
            )
        ]
    ]

    layout = [
        [],
        [
            sg.Col(
                coluna1, vertical_alignment="center", element_justification="center"
            ),
            sg.Col(coluna2, vertical_alignment="top"),
        ],
    ]
    return sg.Window("Contador da Loteria!", layout, size=(540, 280), finalize=True)


# process


def obter_numeros_sorteados():

    try:
        numero_concurso = int(values["-CONCURSO-"])
        loteria = values["-LOTERIA-"]
    except:
        sg.popup(
            "Os campos de Loteria e numero do concurso devem estar corretamente preenchidos ;P",
            keep_on_top=True,
        )

    tem_erro = False
    erro = lambda: print("concurso nao exsite")

    match loteria:
        case "MegaSena":
            try:
                sortedos = MegaSena(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

        case "LotoFacil":
            try:
                sortedos = LotoFacil(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

        case "Quina":
            try:
                sortedos = Quina(numero_concurso)
            except:
                erro()
                tem_erro = True

        case "LotoMania":
            try:
                sortedos = LotoMania(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

        case "TimeMania":
            try:
                sortedos = TimeMania(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

        case "DuplaSena":
            try:
                sortedos = DuplaSena(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

        case "Federal":
            try:
                sortedos = Federal(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

        case "DiadeSorte":
            try:
                sortedos = DiadeSorte(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

        case "SuperSet":
            try:
                sortedos = SuperSet(numero_concurso).listaDezenas()
            except:
                erro()
                tem_erro = True

    if tem_erro:
        return None

    return sortedos


def solver(game_path):

    sorteados = obter_numeros_sorteados()

    if sorteados == None or game_path == "":
        sg.popup("Adicione suas apostas!", keep_on_top=True)
        return None

    with open(game_path, "r") as jogos:

        cartela = [jogo for jogo in jogos]

        result = ""
        c = 1
        for j in cartela:

            if j in ("", "\n"):
                continue

            jogo = j.split()
            numeros_acertados = [numero for numero in jogo if numero in sorteados]
            result += f"numero de acertos do jogo {c}: {len(numeros_acertados)} \n"
            c += 1

        print(numeros_acertados)
    return result


# window logic
win = window()


def visibilidade_celula_resultado():
    if (values["-LOTERIA-"] and values["-CONCURSO-"] != "") and (
        obter_numeros_sorteados() != None
    ):
        win["-CEL1-"].update(visible=True)
        numeros_sorteados = ", ".join(obter_numeros_sorteados())
        win["-GABARITO-"].update(numeros_sorteados)
    else:
        win["-GABARITO-"].update("")
        win["-CEL1-"].update(visible=False)


while True:
    win, event, values = sg.read_all_windows()

    visibilidade_celula_resultado()

    if event == sg.WIN_CLOSED:
        break

    elif event == "Submit":
        output = solver(game_path=values["-GAME-"])
        if output != None:
            sg.popup(output, title="Total acertos")

    elif event == "Help":
        mensagem = 'certifique-se de que os jogos da loteria contidos no aquivo estejam separados por espaço e tenha um "." no fim de cada linha'
        sg.popup(mensagem)


window.close()
