import React  from 'react'
import CodeMirror from '@uiw/react-codemirror';
import 'codemirror/keymap/sublime';
import 'codemirror/theme/monokai.css';

export function Editor(props){
    const {code} = props
    return <CodeMirror
    value={code}
    options={{
      theme: 'monokai',
      keyMap: 'sublime',
      mode: 'jsx',
    }}
  />
}
