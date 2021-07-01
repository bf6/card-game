export enum ButtonVariant {
  filled,
  outlined,
}

export enum ButtonSize {
  sm,
  lg,
}

export type ButtonProps = {
  label: string
  onClick: any
  variant?: ButtonVariant
  size?: ButtonSize
}
