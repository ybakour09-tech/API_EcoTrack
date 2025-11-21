import clsx from "classnames";
import type { ButtonHTMLAttributes } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "ghost";
};

export const Button = ({
  className,
  children,
  variant = "primary",
  ...props
}: ButtonProps) => (
  <button
    className={clsx(
      "inline-flex items-center justify-center gap-2 rounded-xl px-5 py-2.5 text-sm font-semibold transition-all duration-200",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/30",
      "disabled:cursor-not-allowed disabled:opacity-60",
      "active:scale-[0.98]",
      variant === "primary"
        ? "bg-gradient-to-r from-brand via-brand-600 to-brand-dark text-white shadow-md shadow-brand/30 hover:shadow-glow hover:-translate-y-0.5 hover:scale-[1.02]"
        : "border border-amber-200/80 bg-white/90 text-brand-dark hover:bg-gradient-to-r hover:from-amber-50/90 hover:to-white/90 hover:border-amber-300/80 hover:shadow-sm",
      className
    )}
    {...props}
  >
    {children}
  </button>
);

