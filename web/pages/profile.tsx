import DetailItem from "../components/detail-card";

const ProfilePage = () => {
  // Pull user from localStorage
  let user = JSON.parse(localStorage.getItem("user") || "{}");

  if (!user || !user.edipi) {
    // Ask user for EDIPI
    const edipi = prompt("Please enter your EDIPI:");
    // send a GET request to /users/<EDIPI>
    // ALLOW CORS
    fetch(`/users/${edipi}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        localStorage.setItem("user", JSON.stringify(data));
        user = data;
      })
      .catch((error) => console.error("Error fetching user:", error))
      .then(() => {
        user = null;
      });
  } else {
    console.log(user);
  }
  if (!user) {
    user = {
      firstName: "FirstName",
      lastName: "LastName",
      mi: "MI",
      edipi: "1234567890",
      bilmos: "BILMOS123",
      pmos: "PMOS123",
      rank: "PFC",
      dor: "20220101", // Date of Rank in YYYYMMDD format
      id: "0", // Placeholder for user ID
    };
  }
  return (
    <>
      <div className="p-4">
        {/* Current User */}
        <div className="mt-6 p-6 rounded-xl shadow-md border border-gray-100">
          <h2 className="text-2xl font-bold mb-4 pb-2 border-b border-gray-200">
            Current User
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* User Profile Header */}
            <div className="md:col-span-2 flex items-center space-x-4 mb-4">
              <div className="bg-blue-100 text-blue-800 rounded-full w-12 h-12 flex items-center justify-center font-bold text-lg">
                {user.firstName.charAt(0)}
                {user.lastName.charAt(0)}
              </div>
              <div>
                <h3 className="text-xl font-semibold ">
                  {user.rank} {user.firstName} {user.mi && `${user.mi}.`}{" "}
                  {user.lastName}
                </h3>
                <p className="">EDIPI: {user.edipi}</p>
              </div>
            </div>

            {/* User Details Grid */}
            <DetailItem label="BILMOS" value={user.bilmos} />
            <DetailItem label="PMOS" value={user.pmos} />
            <DetailItem label="Rank" value={user.rank} />
            <DetailItem label="DOR" value={formatDate(user.dor)} />
          </div>
        </div>
      </div>
    </>
  );
};

// Date formatter helper
function formatDate(dateNum: string): string {
  const dateStr = dateNum.toString();
  if (dateStr.length !== 8) return dateNum;

  const year = dateStr.substring(0, 4);
  const month = dateStr.substring(4, 6);
  const day = dateStr.substring(6, 8);

  return `${month}/${day}/${year}`;
}
export default ProfilePage;
