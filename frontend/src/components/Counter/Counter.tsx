import React from 'react'
import { CounterProps } from './Counter.types'

const Counter: React.FC<CounterProps> = ({ count, unit }) => {
  return (
    <div className="flex flex-col justify-center items-center bg-black p-4 w-36 h-24 border border-gold text-white font-courier-prime">
      <h2 className="text-5xl">{count}</h2>
      <p className="text-center">{unit}</p>
    </div>
  )
}

export { Counter }
