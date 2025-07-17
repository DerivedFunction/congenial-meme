/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";

// Type for db.json response
interface DbJsonResponse {
  tables: string[];
}

const DatabasePage = () => {
  const [tables, setTables] = useState<string[]>([]);
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
      console.log("Query result:", data); // return array object ex. [[{name:""},{name:""}], [{name:""},{name:""}]], each array is the result of each statement
      generateTable(data);
    } catch (error) {
      console.error("Error fetching tables:", error);
    }
  };
  
  const generateTable = (data: any[]) => {
    const resultsDiv = document.getElementById("results");
    if (!resultsDiv || data.length === 0) return;

    // Get the last array (last executed statement)
    const lastResult = data[data.length - 1];
    if (!lastResult || lastResult.length === 0) {
      resultsDiv.innerHTML = "<p>No results</p>";
      return;
    }

    // Get column names from the first row
    const columns = Object.keys(lastResult[0]);
    let tableHTML =
      "<table class='w-full mt-2 border-collapse border border-gray-300 dark:border-gray-600'><thead><tr class='bg-gray-100 dark:bg-gray-700'>";

    // Add column headers
    tableHTML +=
      "<th class='border border-gray-300 dark:border-gray-600 p-2'>#</th>";
    columns.forEach((col) => {
      tableHTML += `<th class='border border-gray-300 dark:border-gray-600 p-2'>${col}</th>`;
    });
    tableHTML += "</tr></thead><tbody>";

    // Add rows
    lastResult.forEach((row: any, index: number) => {
      tableHTML += "<tr class='hover:bg-gray-50 dark:hover:bg-gray-700'>";
      tableHTML += `<td class='border border-gray-300 dark:border-gray-600 p-2'>${
        index + 1
      }</td>`;
      columns.forEach((col) => {
        tableHTML += `<td class='border border-gray-300 dark:border-gray-600 p-2'>${
          row[col] !== null ? row[col] : "NULL"
        }</td>`;
      });
      tableHTML += "</tr>";
    });

    tableHTML += "</tbody></table>";
    resultsDiv.innerHTML = tableHTML;

    // Add download buttons
    resultsDiv.innerHTML += `
      <div class="mt-2 flex space-x-2">
        <button class="p-2 bg-green-500 text-white rounded-md">Download CSV</button>
        <button class="p-2 bg-green-500 text-white rounded-md">Download JSON</button>
        <button class="p-2 bg-purple-500 text-white rounded-md">Download MD Table</button>
      </div>`;
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
              const query = document.getElementById("query") as HTMLTextAreaElement;
              query.value = `SELECT * FROM ${table};`;
              runQuery();
            }}
          >
            {table}
          </button>
        ))}
      </div>
      
        <h2 className="text-xl font-semibold mt-4">SQL Query</h2>
        <textarea id="query" className="w-full p-2 mt-2 resize-none border-2 rounded-md border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"></textarea>
        <div className="mt-4">
          <button className="p-2 border-1 rounded-md border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
            onClick={runQuery}>
            Run Query
          </button>
      </div>
      <div id="results"></div>
      </div>
    );
};


export default DatabasePage;