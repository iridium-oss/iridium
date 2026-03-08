import { useId } from "react";

type IconProps = {
  name: string;
  className?: string;
  size?: 18 | 20 | 24 | 28 | 36 | 48;
  "aria-hidden"?: boolean;
};

const SIZE_MAP = { 18: "text-[18px]", 20: "text-xl", 24: "text-2xl", 28: "text-[28px]", 36: "text-4xl", 48: "text-5xl" };

export function Icon({ name, className = "", size = 24, "aria-hidden": ariaHidden = true }: IconProps) {
  const id = useId();
  return (
    <span
      className={`material-symbols-outlined inline-block ${SIZE_MAP[size]} ${className}`}
      aria-hidden={ariaHidden}
      aria-labelledby={ariaHidden ? undefined : id}
    >
      {name}
    </span>
  );
}
