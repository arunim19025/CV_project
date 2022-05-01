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
# extra STUFF




#'------------------------------------------------------------------------------------------------------------------------------------------------'#
# App CODE



class app:
    def __init__(self):
        self.btype = ''
        self.ftype = ''
        self.imgs = None


    def overlay(self, surface, base, fabric):
        sz = (600, 600)
        cll = [1, 1 , 10, 1, 1]
        if(surface == 'walls'):
            sz = (1200, 800)
        if(surface == 'cushions'):
            cll[1] = 4

        path = 'output/' + surface + '/' + base + fabric + '.png'
        result = Image.open(path).resize(sz)
        colcol = st.columns(cll)
        colcol[2].image(result, caption = base + ' ' + fabric)


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
                self.overlay(surface, base, fabric)



appobj = app()
appobj.run()

