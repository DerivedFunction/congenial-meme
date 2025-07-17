/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import ResultsTable from "../components/results-table";

// Type for db.json response
interface DbJsonResponse {
  tables: string[];
}

const DatabasePage = () => {
  const [tables, setTables] = useState<string[]>([]);
  const [results, setResults] = useState<any[]>([]);
  const [order, setOrder] = useState(
    "rank firstName mi lastName edipi bilmos pmos dor desc"
  );
  const fetchTables = async () => {
    try {
      const response = await fetch("/tables");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data: DbJsonResponse = await response.json();
      if (!data.tables || !Array.isArray(data.tables)) {
        throw new Error("Invalid db.json format");
      }
      console.log("Tables fetched:", data.tables);
      setTables(data.tables);
    } catch (error) {
      console.error("Error fetching tables:", error);
    }
  };
  const runQuery = async () => {
    try {
      const query = document.getElementById("query") as HTMLTextAreaElement;
      const queryValue = query.value;
      console.log("Query value:", queryValue);
      const response = await fetch("/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: queryValue }),
      });
      if (!response.ok) throw new Error("Query failed");
      const data = await response.json();
      setResults(data);
      console.log("Query result:", data); // return array object ex. [[{name:""},{name:""}], [{name:""},{name:""}]], each array is the result of each statement
    } catch (error) {
      console.error("Error fetching tables:", error);
    }
  };
  

  return (
    <div>
      <h1 className="text-2xl font-bold">SQLite DB Manager</h1>

      <div className="w-full flex justify-end">
        <button
          className="p-2 border-1 rounded-md border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
          onClick={fetchTables}
        >
          Fetch Tables
        </button>
      </div>
      <div>
        {tables.map((table) => (
          <button
            key={table}
            className="p-2 border-1 rounded-md border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 mr-2 mt-2"
            onClick={() => {
              const query = document.getElementById(
                "query"
              ) as HTMLTextAreaElement;
              query.value = `SELECT * FROM ${table};`;
              runQuery();
            }}
          >
            {table.toUpperCase()}
          </button>
        ))}
      </div>

      <h2 className="text-xl font-semibold mt-4">SQL Query</h2>
      <textarea
        id="query"
        className="w-full p-2 mt-2 resize-none border-2 rounded-md border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
      ></textarea>
      <div className="flex w-full">
        <span className="p-2 mt-2">Order: </span>
        <input
          type="text"
          defaultValue={order}
          onChange={(e) => setOrder(e.target.value)}
          className="w-full p-2 mt-2 resize-none border-2 rounded-md border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
        ></input>
      </div>
      <div className="mt-4">
        <button
          className="p-2 border-1 rounded-md border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
          onClick={runQuery}
        >
          Run Query
        </button>
      </div>
      <ResultsTable data={results} order={ order} />
    </div>
  );
};


export default DatabasePage;