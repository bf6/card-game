import { PlayingCardRank, PlayingCardSuit } from '../../constants'

export type PlayingCardProps = {
  rank: PlayingCardRank
  suit: PlayingCardSuit
  style?: any
  className?: string
}
