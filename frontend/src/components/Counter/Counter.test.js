import React from 'react'
import ReactDOM from 'react-dom'
import { Counter } from './Counter'

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
    ReactDOM.render(<Counter unit="Tests" count={1} />, container)
  })

  it('renders units correctly', () => {
    ReactDOM.render(<Counter unit="Eggs" count={12} />, container)
    const counter = container.querySelector('p')
    expect(counter.textContent).toBe('Eggs')
  })

  it('renders count correctly', () => {
    ReactDOM.render(<Counter unit="Eggs" count={12} />, container)
    const counter = container.querySelector('h2')
    expect(counter.textContent).toBe('12')
  })
})
