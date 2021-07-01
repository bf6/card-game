import _ from 'lodash'
import React from 'react'
import { useMediaQuery } from 'react-responsive'
import winner from '../../assets/winner.svg'
import { PlayingCardSuit, PlayingCardRank } from '../../constants'
import { CardGameStatus } from './CardGame.types'
import { LargeFilledButton, SmallOutlinedButton } from 'components/Button/Button'
import { Counter } from 'components/Counter/Counter'
import { PlayingCard } from 'components/PlayingCard/PlayingCard'

// Build the standard 52-card deck
const standardDeck = _.flatten(
  _.values(PlayingCardSuit).map((suit) => _.values(PlayingCardRank).map((rank) => ({ suit, rank })))
)

type Card = {
  rank: PlayingCardRank
  suit: PlayingCardSuit
}

const CardGame: React.FC = () => {
  const [status, setStatus] = React.useState<CardGameStatus>(CardGameStatus.PLAYING)
  const [cardsLeft, setCardsLeft] = React.useState<Array<Card>>(_.shuffle(standardDeck))
  const [hand, setHand] = React.useState<Array<Card>>([])
  const isDesktop = useMediaQuery({ query: '(min-width: 760px)' })

  const dealCards = (count = 5) => {
    const newHand = _.take(cardsLeft, count) // Does not mutate cardsLeft
    const newCardsLeft = cardsLeft.slice(count)
    setCardsLeft(newCardsLeft)
    setHand(newHand)
  }

  const reset = () => {
    setStatus(CardGameStatus.PLAYING)
    setHand([])
    setCardsLeft(_.shuffle(standardDeck))
  }

  const renderDesktopCards = (cards: Array<Card>) => (
    // Pardon the magic numbers
    <div className="relative top-[-90vw]">
      {cards.map((card, i) => {
        const rotation = (2 - i) * 10
        return (
          <PlayingCard
            key={`card-${i}`}
            style={{
              position: 'absolute',
              transform: `translateX(-50%) rotate(${rotation}deg) translateY(83vw)`,
            }}
            {...card}
          />
        )
      })}
    </div>
  )

  const renderMobileCards = (cards: Array<Card>) => (
    <div className="flex flex-wrap justify-center mb-20">
      {cards.map((card, i) => (
        <PlayingCard key={`card-${i}`} {...card} />
      ))}
    </div>
  )

  const isLastHand = () => cardsLeft.length <= 0

  React.useEffect(() => {
    dealCards()
  }, [])

  React.useEffect(() => {
    if (isLastHand()) {
      if (_.some(hand, (card) => card.rank === PlayingCardRank.ACE)) {
        setStatus(CardGameStatus.WIN)
      } else {
        setStatus(CardGameStatus.LOSS)
      }
    }
  }, [hand])

  return (
    <div className="flex justify-between flex-col p-10 bg-gradient-to-b from-grass to-grass-dark min-h-screen items-center">
      <div className="mb-8">
        <Counter unit="Cards Left" count={Math.max(0, cardsLeft.length)} />
      </div>
      {status === CardGameStatus.WIN && (
        <div className="absolute max-w-100 top-32 z-index-3">
          <img src={winner} alt="Winner banner" />
        </div>
      )}
      {/* There must be a better way to do this */}
      {isDesktop && !isLastHand() ? renderDesktopCards(hand) : renderMobileCards(hand)}
      {status === CardGameStatus.LOSS && (
        <div className="text-xl font-courier-prime text-center text-white">
          <p>You lose.</p>
          <p>Better luck next time!</p>
        </div>
      )}
      <div className="flex flex-col w-full">
        <div className="mb-4 self-center">
          {status === CardGameStatus.PLAYING ? (
            <LargeFilledButton label="DEAL" onClick={() => dealCards()} />
          ) : (
            <SmallOutlinedButton label="Play again" onClick={() => reset()} />
          )}
        </div>
        {status === CardGameStatus.PLAYING && (
          <div className="self-center md:self-end ">
            <SmallOutlinedButton label="Reset" onClick={() => reset()} />
          </div>
        )}
      </div>
    </div>
  )
}

export { CardGame }
