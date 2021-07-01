import React from 'react'
import ReactDOM from 'react-dom'
import { SmallOutlinedButton, LargeFilledButton } from './Button'

let container = null

beforeEach(() => {
  container = document.createElement('div')
  document.body.appendChild(container)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

describe('SmallOutlineButton', () => {
  it('renders without crashing', () => {
    ReactDOM.render(<SmallOutlinedButton label="Test SOB" onClick={jest.fn()} />, container)
  })

  it('renders labels correctly', () => {
    const label = 'Test SOB'
    ReactDOM.render(<SmallOutlinedButton label={label} onClick={jest.fn()} />, container)
    const button = container.querySelector('button')
    expect(button.textContent).toBe(label)
  })
})

describe('LargeFilledButton', () => {
  it('renders without crashing', () => {
    ReactDOM.render(<LargeFilledButton label="Test LFB" onClick={jest.fn()} />, container)
  })

  it('renders labels correctly', () => {
    const label = 'Test LFB'
    ReactDOM.render(<LargeFilledButton label={label} onClick={jest.fn()} />, container)
    const button = container.querySelector('button')
    expect(button.textContent).toBe(label)
  })
})
