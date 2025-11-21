import clsx from "classnames";

type CardProps = {
  title?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
};

export const Card = ({ title, actions, children, className }: CardProps) => (
  <section
    className={clsx(
      "rounded-2xl border border-amber-100/60 bg-white/90 p-6 shadow-soft backdrop-blur-md",
      "card-hover animate-fade-in",
      className
    )}
  >
    {(title || actions) && (
      <header className="mb-5 flex items-center justify-between border-b border-amber-100/40 pb-3">
        {title && (
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-600">
            {title}
          </h3>
        )}
        {actions}
      </header>
    )}
    <div className="animate-slide-up">{children}</div>
  </section>
);

