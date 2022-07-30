export enum SeatType {
  Available = "available",
  Picking = "picking",
  Picked = "picked",
}

type Props = {
  variant: SeatType;
};

export default function Seat(props: Props) {
  let bg = "#494d62";

  switch (props.variant) {
    case SeatType.Available:
      bg = "#494d62";
      break;
    case SeatType.Picking:
      bg = "#f25660";
    case SeatType.Picked:
      bg = "#4b4c62";
      break;
  }

  return <div className={`w-6 h-4 bg-[${bg}] rounded-t-lg`} />;
}
