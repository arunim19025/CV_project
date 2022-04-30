import os
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image


#'------------------------------------------------------------------------------------------------------------------------------------------------'#
# GLOBAL STUFF

surfaces = dict()

for surface in os.listdir('dataset'):
    surfaces[surface] = dict()
    for itype in os.listdir('dataset/' + surface):
        surfaces[surface][itype] = dict()
        for filename in os.listdir('dataset/' + surface + '/' + itype):
            name = filename.split('.')[0]
            print(itype, name)
            surfaces[surface][itype][name] = Image.open('dataset/' + surface + '/' + itype + '/' + filename)


#'------------------------------------------------------------------------------------------------------------------------------------------------'#
# FUNCTIONS and STUFF

def construct_sidebar(blabels, flabels):
    st.sidebar.markdown(
        '<p class="header-style">Choose Base and Fabric</p>',
        unsafe_allow_html=True
    )
    base = st.sidebar.selectbox(
        'Select base image',
        blabels
    )

    fabric = st.sidebar.selectbox(
        'Select fabric',
        flabels
    )

    values = [base, fabric]

    return values


#'------------------------------------------------------------------------------------------------------------------------------------------------'#

class app:
    def __init__(self):
        self.btype = ''
        self.ftype = ''
        self.imgs = None


    def overlay(self, base, fabric):
        st.write(base, fabric)
        return 'overlaid image'


    def construct_sidebar(self, blabels, flabels):
        st.sidebar.markdown(
            '<p class="header-style">Choose Base and Fabric</p>',
            unsafe_allow_html=True
        )

        surface = st.sidebar.selectbox(
            'Select type of surface',
            ['curtains', 'cushions', 'walls']
        )

        base = st.sidebar.selectbox(
            'Select base image',
            blabels
        )

        fabric = st.sidebar.selectbox(
            'Select fabric',
            flabels
        )

        values = [surface, base, fabric]

        return values


    def run(self):
        isize = (250, 250)

        st.title('Interior Designing Texture Overlay')
        st.write('This app aims to implement texture overlay on specific interior designing components, mainly cushions, bedsheets, curtains, and walls')
        st.write('')

        blabels = ['base1', 'base2', 'base3', 'base4', 'base5']
        flabels = ['fabric1', 'fabric2', 'fabric3', 'fabric4', 'fabric5']

        surface, base, fabric = self.construct_sidebar(blabels, flabels)
        self.imgs = surfaces[surface]
        images = self.imgs
        st.write('')
        st.write('')
        st.write('')

        blen = len(images['base'])
        flen = len(images['fabric'])

        colsb = st.columns(blen + 1)
        colsb[0].subheader('Choose base image')

        for i in range(1, blen+1):
            colsb[i].image(images['base'][blabels[i-1]].resize(isize), caption=blabels[i-1])
        
        st.write('')
        st.write('')
        st.write('')

        colsf = st.columns(flen+1)
        colsf[0].subheader('Choose fabric')

        for i in range(1, flen+1):
            colsf[i].image(images['fabric'][flabels[i-1]].resize(isize), caption=flabels[i-1])

        st.write('')
        st.write('')
        st.write('')


        bidx = int(base[-1])
        fidx = int(fabric[-1])

        if(bidx > blen or fidx > flen):
            st.subheader('Invalid selection, please change your choices')
        else:
            colsplit = st.columns(21)
            if(colsplit[10].button('OVERLAY')):
                results = self.overlay(base, fabric)
                st.write(results)




appobj = app()
appobj.run()





# st.title('Interior Designing Texture Overlay')
# st.write('This app aims to implement texture overlay on specific interior designing components, mainly cushions, bedsheets, curtains, and walls')
# st.write('')


# curtainimage = Image.open('dataset/curtains/base/base3.jpg')
# cushionimage = Image.open('dataset/cushions/base/base4.jpg')
# wallimage = Image.open('assets/extrawall.jpg')
# ill = [curtainimage, cushionimage, wallimage]
# caption = ['curtain', 'cushion', 'wall']


# surfaceselected = False

# cols = st.columns([1, 1, 1])
# cols[0].image(ill[0], width=500)
# if(cols[0].button(caption[0])):
#     images = surfaces['curtains']
#     surfaceselected = True
# cols[1].image(ill[1], width=500)
# if(cols[1].button(caption[1])):
#     images = surfaces['cushions']
#     surfaceselected = True
# cols[2].image(ill[2], width=500)
# if(cols[2].button(caption[2])):
#     images = surfaces['walls']
#     surfaceselected = True

# if(surfaceselected):
#     st.write('')
#     st.write('')
#     st.write('')


#     blen = len(images['base'])
#     flen = len(images['fabric'])
#     blabels = ['base1', 'base2', 'base3', 'base4', 'base5', 'base6']
#     flabels = ['fabric1', 'fabric2', 'fabric3', 'fabric4', 'fabric5', 'fabric6']


#     colsb = st.columns(blen + 1)
#     colsb[0].header('Choose base image')

#     btype = colsb[0].selectbox('BASES', blabels[:blen], on_change=overlayer)
#     for i in range(1, blen+1):
#         colsb[i].image(images['base'][blabels[i-1]].resize((300, 300)), width=300, caption=blabels[i-1])


#     st.write('')
#     st.write('')
#     st.write('')

#     colsf = st.columns(flen+1)
#     colsf[0].header('Choose fabric')

#     ftype = colsf[0].selectbox('FABRICS', flabels[:flen], on_change=overlayer)
#     for i in range(1, flen+1):
#         colsf[i].image(images['fabric'][flabels[i-1]], width=300, caption=flabels[i-1])

