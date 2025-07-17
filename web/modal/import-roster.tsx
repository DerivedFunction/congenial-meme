const ImportModal = () => {
  // A center popup
  return (
    <div className="absolute flex items-center justify-center h-screen w-full border-1 bg-white dark:bg-gray-900">
      <h1>Import Roster</h1>
      <form>
        <input type="file" accept=".csv, .xlsx" />
        <button type="submit">Import</button>
      </form>
    </div>
  );
};

export default ImportModal;
