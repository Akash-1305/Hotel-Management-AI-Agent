export interface BookingData {
  RoomId: number;
  type: string;
  price: number;
  FirstName: string;
  LastName: string;
  arrivalDate: string;
  departureDay: string;
  booking_price: number;
  discount: number;
  PaymentType: string;
  payment_completed: number;
}

export interface OccupancyData {
  day: string;
  occupancyPercentage: number;
}

export interface MetricData {
  title: string;
  value: string | number;
  icon: string;
  color: string;
  bgColor: string;
}