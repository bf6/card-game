import React from 'react'
import ReactDOM from 'react-dom'
import { act } from 'react-dom/test-utils'
import { CardGame } from './CardGame'

let container = null

beforeEach(() => {
  container = document.createElement('div')
  document.body.appendChild(container)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

describe('Counter', () => {
  it('renders without crashing', () => {
    ReactDOM.render(<CardGame />, container)
  })

  it('deals cards', () => {
    ReactDOM.render(<CardGame />, container)
    const counter = container.querySelector('h2.text-5xl')
    expect(counter.textContent).toBe('52')
    const button = container.querySelector('button')
    act(() => {
      button.dispatchEvent(new MouseEvent('click'))
    })
    expect(counter.textContent).toBe('47')
  })
})
