from time import perf_counter, sleep
from py3dbp import Packer, Bin, Item, Painter
from PIL import Image

import pandas as pd
import streamlit as st
import numpy as np
import datetime


###
st.set_page_config(
    page_title='PYPACKT',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={'About': 'PYPACKT ou pyContainer Packt é um programa desenvolvido em python para optimizar o processo de organizar blocos num container.'}
)

st.set_option('deprecation.showPyplotGlobalUse', False)


@st.cache()
def load_xls(file):
    xls = pd.read_excel(file, sheet_name='packt')
    return xls


def main_packt(packt_bin, file_buff, decimals, algorthm):
    try:
        colors = ['red', 'blue', 'green', 'gray', 'purple']
        xls = load_xls(file_buff)
        for i, (nrbloco, pesobal, pesocal, comp, alt, larg) in enumerate(xls.values):
            color = np.random.choice(colors)
            packt_bin.addItem(
                Item(i, nrbloco, 'cube', (float(comp), float(alt), float(larg)), float(pesobal), 1, 100, True, color))

        if algorthm:
            options = True
        else:
            options = False

        if decimals:
            noptions = 0
        else:
            noptions = 2

        packt_bin.pack(bigger_first=options, distribute_items=100,
                       fix_point=True, number_of_decimals=noptions)

        b = packt_bin.bins[0]

        return b
    except:
        return False


HELP_PNG = 'help.png'
###


st.sidebar.title('PYPACKT')
st.sidebar.subheader('Definições')
menu = st.sidebar.selectbox('MENU', ('APP', 'Solver'))

if menu == 'APP':
    st.title('PYPACKT')
    st.markdown('---')

    st.info('PYPACKT ou pyContainer Packt é um programa desenvolvido em python para optimizar o processo de organizar blocos num container.')
    st.markdown('#### Informações:')
    st.write('Para inicializar o programa, aceda ao painel lateral (definições) e, através do menu, selecione a opção **Solver**.')
    st.write('Para garantir o melhor funcionamento do **PYPACKT**, considere organizar a planilha **EXCEL** conforme apresentado na figura, com a nomeação da folha como "packt" (minúsculas e sem aspas).')
    st.image(Image.open(HELP_PNG),
             caption='Arquivo **EXCEL** devidamente formatado e reconhecido pelo programa', use_column_width=True)

if menu == 'Solver':
    hist = list()

    decimals = st.sidebar.checkbox(
        'Inteiros', help='Converter números com pontos decimais em inteiros', value=True)

    algorthm = st.sidebar.checkbox(
        'BestFit', help='Usar algoritmo de heurística gulosa para solucionar o problema', value=True)

    buff_file = st.sidebar.file_uploader(
        'Carregar arquivo', type=['xls', 'xlsx'])

    st.sidebar.markdown('---')
    st.sidebar.subheader('Propriedades do Container')
    container_nome = st.sidebar.text_input(
        'ID / Nome', placeholder='Examplo1234', max_chars=20)
    container_peso = float(st.sidebar.number_input(
        'Peso (Kg)', min_value=0.0, max_value=1000000.0, step=1000.0, value=40000.0))
    container_compr = float(st.sidebar.number_input(
        'Comprimento (m)', min_value=0.0, max_value=100000.0, step=1.0, value=15.0))
    container_altur = float(st.sidebar.number_input(
        'Altura (m)', min_value=0.0, max_value=100000.0, step=1.0, value=5.0))
    container_largr = float(st.sidebar.number_input(
        'Largura (m)', min_value=0.0, max_value=100000.0, step=1.0, value=8.0))
    st.sidebar.markdown('---')

    st.title('PYPACKT')
    st.markdown('---')
    st_info = st.empty()

    if container_nome == '':
        st_info.warning(
            '**ID / Nome** em **Propriedades do Container** situado no painel lateral, é um campo obrigatório.')

    elif buff_file is not None:
        st_info.info('Tudo pronto! Inicializar')
    else:
        st_info = st.warning(
            'Carregue um arquivo excel usando o painel lateral, em definições')

    btn_i = st.button('Inicializar')

    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    volume_disp = float(container_compr * container_altur * container_largr)

    st.metric('Volume total (disponível)', value=f'{volume_disp:.2f} m³')

    with col1:
        st.metric('Peso', value=f'{(float(container_peso) / 1000):.2f} t')

    with col2:
        st.metric('Comprimento', value=f'{float(container_compr):.2f} m')

    with col3:
        st.metric('Altura', value=f'{float(container_altur):.2f} m')

    with col4:
        st.metric('Largura', value=f'{float(container_largr):.2f} m')

    packt = Packer()
    box = Bin(container_nome, (float(container_compr), float(container_altur),
              float(container_largr)), float(container_peso), 0, 0)
    packt.addBin(box)
    b = packt.bins[0]
    painter = Painter(b)

    if btn_i and buff_file is not None and container_nome != '':
        st_info.warning('Aguarde...')
        with st.spinner('A Processar...'):
            start = perf_counter()
            b = main_packt(packt_bin=packt, file_buff=buff_file,
                           decimals=decimals, algorthm=algorthm)
            eta = perf_counter() - start
            sleep(3)

        if b:
            painter = Painter(b)
            painter.plotBoxAndItems()
            st.pyplot()
            st_info.success('Feito!')
            st.markdown('---')
            st.write('# RESUMO')
            col1, col2 = st.columns([3, 3], gap='large')
            volume_t = 0
            volume_t_itens = 0
            volume_weights = 0
            with col1:
                st.markdown('### **#Selecionado(s)**')
                st.markdown('---')
                nr_order = 0

                for item in b.items:

                    nr_order += 1
                    st.write(f'ID : {item.partno}')
                    st.write(f'Nr. Bloco : {item.name}')
                    st.write(
                        f'Posição (x, y, z) : ({item.position[0]}, {item.position[1]}, {item.position[2]})')
                    st.write(f'Peso : {(float(item.weight) / 1000):.2f} t')
                    st.write(
                        f'Volume : {float(item.width * item.height * item.depth):.2f} m³')
                    st.write(
                        f'Comprimento x Altura x Largura : {item.width} x {item.height} x {item.depth}')
                    volume_t += float(item.width) * \
                        float(item.height) * float(item.depth)
                    volume_t_itens += 1
                    volume_weights += item.weight
                    hist.append((item.name, float(item.weight), float(item.width), float(item.height), float(
                        item.depth), (float(item.width) * float(item.height) * float(item.depth)), nr_order))
                    st.markdown('---')

            with col2:
                st.markdown('### **#Estatísticas**')
                st.write(f'Volume total (ocupado) : {volume_t:.2f} m³')
                st.write(
                    f'Percentual de Volume (ocupado) : {(round(volume_t / volume_disp * 100, 2)):.2f} %')
                st.write(
                    f'Volume (restante) : {(volume_disp - volume_t):.2f} m³')
                st.write(f'Bloco(s) : {volume_t_itens}')
                st.write(
                    f'Peso (a carregar) : {float(volume_weights) / 1000.0} t')
                st.write(f'Distribuição de peso (gravidade) : {b.gravity}')
                unit = 's'
                if eta < 1:
                    unit = 'ms'
                    eta *= 1000.0

                st.write(f'Processado em : {eta:.3f} {unit}')
                df = pd.DataFrame(hist, columns=[
                                  'Nr. Bloco', 'Peso Balança', 'Comp.', 'Alt.', 'Larg.', 'Volume (Cub.)', 'Ordem'])
                temp = f'{hash(datetime.date.today())}_{container_nome}.xlsx'
                df.to_excel(
                    f'./relatorios/{temp}', sheet_name='packt', float_format='%.2f', index=False)
                st.success(f'Relatório criado com sucesso! Arquivo : {temp}')

        else:
            st_info.error(
                'Algo errado! Considere ajustar as propriedades do container ou se assegure que o ficheiro **EXCEL** encontra-se formatado conforme se apresenta na figura :')
            st.image(Image.open(
                HELP_PNG), caption='Arquivo **EXCEL** devidamente formatado e reconhecido pelo programa', use_column_width=True)

    else:
        st.pyplot(painter.plotBoxAndItems())
