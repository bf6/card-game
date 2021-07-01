import _ from 'lodash'
import React from 'react'
import { SuitIconMap, PlayingCardSuit } from '../../constants'
import { PlayingCardProps } from './PlayingCard.types'

const PlayingCard: React.FC<PlayingCardProps> = ({ rank, suit, style = null, className = '' }) => {
  const fontColorStyle = _.includes([PlayingCardSuit.DIAMOND, PlayingCardSuit.HEART], suit)
    ? 'text-red-500'
    : 'text-black'

  return (
    <div
      className={`flex m-2 flex-col justify-between bg-white p-4 rounded-xl w-24 h-36 xl:w-36 xl:h-52 shadow-2xl ${className}`}
      style={style}
    >
      <div className="flex flex-col items-center w-1/3">
        <h2
          className={`font-courier-prime text-4xl xl:text-6xl tracking-tighter ${fontColorStyle}`}
        >
          {rank}
        </h2>
        <img className="w-2/3" src={SuitIconMap[suit]} alt="Card suit small" />
      </div>
      <img className="w-3/4 self-end" src={SuitIconMap[suit]} alt="Card suit large" />
    </div>
  )
}

export { PlayingCard }
