import { useState } from "react";

// Type for db.json response
interface DbJsonResponse {
  tables: string[];
}

// Type for table row data (flexible for any key-value pairs)
interface TableRow {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any; // Allows for dynamic columns like firstName, lastName, etc.
}

// Type for tableData state
interface TableData {
  [tableName: string]: TableRow[];
}

const DatabasePage = () => {
  const [tables, setTables] = useState<string[]>([]);
  const [tableData, setTableData] = useState<TableData>({});

  const fetchTables = async () => {
    try {
      const response = await fetch("/static/db.json");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data: DbJsonResponse = await response.json();
      if (!data.tables || !Array.isArray(data.tables)) {
        throw new Error("Invalid db.json format");
      }
      console.log("Tables fetched:", data.tables);
      setTables(data.tables);

      // Fetch data for each table
      const tableDataPromises = data.tables.map(async (table: string) => {
        try {
          const tableResponse = await fetch(`/${table}`);
          if (!tableResponse.ok) {
            throw new Error(`Failed to fetch table: ${table}`);
          }
          const tableData: TableRow[] = await tableResponse.json();
          return { tableName: table, data: tableData };
        } catch (error) {
          console.error(`Error fetching table ${table}:`, error);
          return { tableName: table, data: [] };
        }
      });

      const results = await Promise.all(tableDataPromises);
      const newTableData = results.reduce(
        (acc, { tableName, data }) => ({
          ...acc,
          [tableName]: data,
        }),
        {} as TableData
      );
      setTableData(newTableData);
    } catch (error) {
      console.error("Failed to fetch tables:", error);
    }
  };

  // Component to render a single table
  const TableView: React.FC<{ tableName: string; data: TableRow[] }> = ({
    tableName,
    data,
  }) => {
    if (!data || data.length === 0) {
      return <div>No data available for {tableName}</div>;
    }

    // Get column headers from the first row
    const columns = Object.keys(data[0]);

    return (
      <div className="mt-4">
        <h3 className="text-lg font-semibold mb-2">{tableName}</h3>
        <table className="w-full border-collapse">
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column} className="border p-2">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                {columns.map((column) => (
                  <td key={column} className="border p-2">
                    {row[column] ?? "N/A"} {/* Handle undefined/null values */}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="flex">
      {/* Main content */}
      <div className="flex-1 p-4">
        <h1>SQLite DB Management</h1>
        <div className="flex flex-col space-y-4">
          <button
            onClick={fetchTables}
            className="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition-colors"
          >
            Fetch Tables
          </button>
          {/* Render all table data */}
          {Object.entries(tableData).map(([tableName, data]) => (
            <TableView key={tableName} tableName={tableName} data={data} />
          ))}
        </div>
      </div>
      {/* Right sidebar */}
      <div className="w-64 p-4 bg-gray-100">
        <h2 className="text-lg font-semibold">Tables</h2>
        <ul className="list-disc pl-5">
          {tables.map((table, index) => (
            <li key={index} className="py-1">
              {table}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DatabasePage;
