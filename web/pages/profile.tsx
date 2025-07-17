/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";
import DetailItem from "../components/detail-card";

const ProfilePage = () => {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");

    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser?.edipi) {
          setUser(parsedUser);
          return;
        }
      } catch (e) {
        console.error("Error parsing user from localStorage:", e);
      }
    }

    // Ask for EDIPI
    const edipi = prompt("Please enter your EDIPI:");
    if (!edipi) return;

    fetch(`/users/${edipi}`)
      .then((res) => res.json())
      .then((data) => {
        localStorage.setItem("user", JSON.stringify(data));
        setUser(data);
      })
      .catch((error) => console.error("Error fetching user:", error));
  }, []);

  // Default fallback user (optional)
  const displayUser = user ?? {
    firstName: "FirstName",
    lastName: "LastName",
    mi: "MI",
    edipi: "1234567890",
    bilmos: "0000",
    pmos: "0000",
    rank: "PFC",
    dor: "20250101",
    id: "0",
  };

  return (
    <div className="p-4">
      <div className="mt-6 p-6 rounded-xl shadow-md border border-gray-100">
        <h2 className="text-2xl font-bold mb-4 pb-2 border-b border-gray-200">
          Current User
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2 flex items-center space-x-4 mb-4">
            <div className="bg-blue-100 text-blue-800 rounded-full w-12 h-12 flex items-center justify-center font-bold text-lg">
              {displayUser.firstName.charAt(0)}
              {displayUser.lastName.charAt(0)}
            </div>
            <div>
              <h3 className="text-xl font-semibold">
                {displayUser.rank} {displayUser.firstName}{" "}
                {displayUser.mi && `${displayUser.mi}.`} {displayUser.lastName}
              </h3>
              <p>EDIPI: {displayUser.edipi}</p>
            </div>
          </div>

          <DetailItem label="BILMOS" value={displayUser.bilmos} />
          <DetailItem label="PMOS" value={displayUser.pmos} />
          <DetailItem label="Rank" value={displayUser.rank} />
          <DetailItem label="DOR" value={formatDate(displayUser.dor)} />
        </div>
      </div>
    </div>
  );
};

function formatDate(dateNum: string): string {
  const dateStr = dateNum.toString();
  if (dateStr.length !== 8) return dateNum;

  const year = dateStr.substring(0, 4);
  const month = dateStr.substring(4, 6);
  const day = dateStr.substring(6, 8);

  return `${month}/${day}/${year}`;
}

export default ProfilePage;
