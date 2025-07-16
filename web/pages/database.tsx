const DatabasePage = () => {
  // Pull user from localStorage
  let user = localStorage.getItem("user");
  if (!user) {
    // Ask user for EDIPI
    user = prompt("Please enter your EDIPI:");
    // send a GET request to /users/<EDIPI>
    // ALLOW CORS
    fetch(`/users/${user}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        localStorage.setItem("user", JSON.stringify(data));
      })
      .catch((error) => console.error("Error fetching user:", error));
  } else {
    user = JSON.parse(user);
    console.log(user);
  }

  return (
    <>
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Manage SQLite Database</h1>
        <p className="text-gray-700">
          This is where you can manage your SQLite database.
        </p>
        {/* Current User */}
        <div className="mt-4">
          <h2 className="text-xl font-bold mb-2">Current User</h2>
          <p className="text-gray-700">
            Details about the current user profile.
          </p>
        </div>
      </div>
    </>
  );
};

export default DatabasePage;
