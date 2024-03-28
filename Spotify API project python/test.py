import streamlit as st

# Title
st.title('My First Streamlit App')

name = st.text_input('Enter your name')
st.write(f'Hello, {name}!')

# Header
st.header('This is a header')

# Subheader
st.subheader('This is a subheader')

# Text
st.write('Hello, world!')

# Markdown
st.markdown('**This** is some markdown _text_.')

# Button
if st.button('Click me'):
    st.write('Button clicked!')

# Checkbox
if st.checkbox('Check me'):
    st.write('Checkbox checked!')

# Selectbox
option = st.selectbox('Select an option', ['Option 1', 'Option 2', 'Option 3'])
st.write('You selected:', option)

# Slider
value = st.slider('Select a value', 0, 100, 50)
st.write('You selected:', value)