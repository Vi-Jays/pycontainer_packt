from time import perf_counter, sleep
from py3dbp import Packer, Bin, Item, Painter
from PIL import Image

import pandas as pd
import streamlit as st
import numpy as np


###
st.set_page_config(
    page_title='PYPACKT',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={'About': 'PYPACKT ou pyContainer Packt é um programa desenvolvido em python para optimizar o processo de organizar blocos num container.'}
)

st.set_option('deprecation.showPyplotGlobalUse', False)


@st.cache
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
        'Inteiros', help='Arredondar números com decimais em inteiros. **RECOMENDADO**', value=True)

    algorthm = st.sidebar.checkbox(
        'BestFit', help='Usar algoritmo de heurística gulosa para solucionar o problema', value=True)

    buff_file = st.sidebar.file_uploader(
        'Carregar arquivo', type=['xls', 'xlsx'])

    st.sidebar.markdown('---')
    st.sidebar.subheader('Propriedades do Container')

    container_cub = 0
    container_compr = 0
    container_altur = 0
    container_largr = 0

    container_nome = st.sidebar.text_input(
        'ID / Nome', placeholder='Examplo1234', max_chars=20)

    containers = []

    container_type = st.sidebar.selectbox(
        'Contentores', ('Standard', 'High Cube'))

    if container_type == 'Standard':
        containers = ["20' ST", "40' ST"]
    if container_type == 'High Cube':
        containers = ["40' HC", "45' HC"]

    container_options = st.sidebar.selectbox(
        'Tipologia', options=containers)

    if container_options == "20' ST":
        container_carga_max = 28_000
        container_compr = 5.898
        container_altur = 2.390
        container_largr = 2.350
        container_cub = 33.000
    if container_options == "40' ST":
        container_carga_max = 26_500
        container_compr = 12.035
        container_altur = 2.393
        container_largr = 2.350
        container_cub = 67.000
    if container_options == "40' HC":
        container_carga_max = 26_510
        container_compr = 12.030
        container_altur = 2.690
        container_largr = 2.350
        container_cub = 76.000
    if container_options == "45' HC":
        container_carga_max = 26_000
        container_compr = 13.556
        container_altur = 2.695
        container_largr = 2.352
        container_cub = 86.000

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

    st.metric('Cubicagem máxima', value=f'{container_cub:.2f} m³')

    with col1:
        st.metric('Carga máxima',
                  value=f'{(float(container_carga_max) / 1000):.2f} t')

    with col2:
        st.metric('Comprimento', value=f'{float(container_compr):.2f} m')

    with col3:
        st.metric('Largura', value=f'{float(container_largr):.2f} m')

    with col4:
        st.metric('Altura', value=f'{float(container_altur):.2f} m')

    packt = Packer()

    box = Bin(container_nome, (container_compr, container_largr,
              container_altur), container_carga_max, 0, 0)

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
                    f'Percentual de Volume (ocupado) : {(round((volume_t / container_cub) * 100, 2)):.2f} %')
                st.write(
                    f'Volume (restante) : {(container_cub - volume_t):.2f} m³')
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
                temp = f'RP_{container_nome}_{hash(container_nome)}.xlsx'
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
