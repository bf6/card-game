import React from 'react'
import ReactDOM from 'react-dom'
import { PlayingCardRank, PlayingCardSuit } from '../../constants'
import { PlayingCard } from './PlayingCard'

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
    ReactDOM.render(
      <PlayingCard rank={PlayingCardRank.ACE} suit={PlayingCardSuit.DIAMOND} />,
      container
    )
  })

  it('renders rank correctly', () => {
    ReactDOM.render(
      <PlayingCard rank={PlayingCardRank.ACE} suit={PlayingCardSuit.DIAMOND} />,
      container
    )
    const card = container.querySelector('h2')
    expect(card.textContent).toBe('A')
  })
})
