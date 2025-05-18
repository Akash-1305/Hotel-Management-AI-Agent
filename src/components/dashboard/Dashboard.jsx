import React from "react";
import { format } from "date-fns";
import { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE } from "../../App";
import {
  Clock,
  Users,
  CheckCircle,
  XCircle,
  DollarSign,
  RefreshCw,
  CalendarPlus,
} from "lucide-react";
import MetricCard from "./MetricCard";
import BookingsTable from "./BookingsTable";

const Dashboard = () => {
  const today = new Date();
  const formattedDate = format(today, "EEEE, MMMM d, yyyy");

  const [bookingList, setBookingList] = useState([]);
  const [vacantRoomCount, setVacantRoomCount] = useState(0);
  const [revenueData, setRevenueData] = useState({});
  const [occupancyDataState, setOccupancyDataState] = useState({});
  const [bookingsStats, setBookingsStats] = useState({});
  const [popularityStats, setPopularityStats] = useState({});

  useEffect(() => {
    getDashboardStats();
    getBookedRooms();
  }, []);

  function getDashboardStats() {
    axios
      .get(API_BASE + `/hotel-statistics`)
      .then((res) => {
        if (res.data && res.data.length > 0) {
          const stats = res.data[0];
          setOccupancyDataState(stats.occupancy || {});
          setRevenueData(stats.revenue || {});
          setBookingsStats(stats.bookings || {});
          setPopularityStats(stats.popularity || {});
          setVacantRoomCount(stats.occupancy?.vacant_rooms || 0);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }

  function getBookedRooms() {
    axios
      .get(API_BASE + `/current-stays`)
      .then((res) => {
        setBookingList(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  return (
    <div>
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">{formattedDate}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <MetricCard
          title="Vacant Rooms"
          value={vacantRoomCount}
          icon={Users}
          color="text-blue-600"
          bgColor="bg-blue-100"
        />
        <MetricCard
          title="Occupied Rooms"
          value={occupancyDataState.occupied_rooms || bookingList.length}
          icon={CheckCircle}
          color="text-green-600"
          bgColor="bg-green-100"
        />
        <MetricCard
          title="Revenue"
          value={`$${(revenueData.total_revenue || 0).toFixed(2)}`}
          icon={DollarSign}
          color="text-green-600"
          bgColor="bg-green-100"
        />
      </div>
      <div className="lg:col-span-2">
        <BookingsTable bookings={bookingList} />
      </div>
    </div>
  );
};

export default Dashboard;
