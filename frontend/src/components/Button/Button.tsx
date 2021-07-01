import React from 'react'
import { ButtonProps, ButtonVariant, ButtonSize } from './Button.types'

const Button: React.FC<ButtonProps> = ({ label, onClick, variant, size }) => {
  const variantClass =
    variant === ButtonVariant.filled
      ? 'bg-gold text-black'
      : 'bg-transparent border-2 border-gold text-gold'
  const sizeClass =
    size === ButtonSize.lg
      ? 'px-12 py-5 text-xl md: text-3xl lg:text-5xl'
      : 'px-6 py-1 text-lg lg:text-xl'
  return (
    <button
      className={`rounded-xl font-alfa-slab-one ${variantClass} ${sizeClass}`}
      type="button"
      aria-label={label}
      onClick={onClick}
    >
      {label}
    </button>
  )
}

const LargeFilledButton: React.FC<ButtonProps> = ({ label, onClick }) => (
  // eslint-disable-next-line jsx-a11y/control-has-associated-label
  <Button label={label} onClick={onClick} variant={ButtonVariant.filled} size={ButtonSize.lg} />
)

const SmallOutlinedButton: React.FC<ButtonProps> = ({ label, onClick }) => (
  // eslint-disable-next-line jsx-a11y/control-has-associated-label
  <Button label={label} onClick={onClick} variant={ButtonVariant.outlined} size={ButtonSize.sm} />
)

export { Button, LargeFilledButton, SmallOutlinedButton }
