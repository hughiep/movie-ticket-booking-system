import Seat, { SeatType } from "~/components/Seat";

export default function Index() {
  return (
    <div className="flex gap-2 w-full h-[100vh] p-8 bg-[#2c2d39]">
      <Seat variant={SeatType.Available} />
      <Seat variant={SeatType.Picked} />
      <Seat variant={SeatType.Picking} />
      <Seat variant={SeatType.Available} />
      <Seat variant={SeatType.Picked} />
      <Seat variant={SeatType.Picking} />
    </div>
  );
}
