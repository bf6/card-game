import Clover from './assets/Clover.svg'
import Diamond from './assets/Diamond.svg'
import Heart from './assets/Heart.svg'
import Spade from './assets/Spade.svg'

export enum PlayingCardRank {
  TWO = '2',
  THREE = '3',
  FOUR = '4',
  FIVE = '5',
  SIX = '6',
  SEVEN = '7',
  EIGHT = '8',
  NINE = '9',
  TEN = '10',
  JACK = 'J',
  QUEEN = 'Q',
  KING = 'K',
  ACE = 'A',
}

export enum PlayingCardSuit {
  CLUB = 'CLUB',
  DIAMOND = 'DIAMOND',
  HEART = 'HEART',
  SPADE = 'SPADE',
}

export const SuitIconMap = {
  [PlayingCardSuit.CLUB]: Clover,
  [PlayingCardSuit.DIAMOND]: Diamond,
  [PlayingCardSuit.HEART]: Heart,
  [PlayingCardSuit.SPADE]: Spade,
}
