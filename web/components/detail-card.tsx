interface DetailItemProps {
  label: string;
  value: string | number;
  highlight?: boolean;
}
// Helper components
const DetailItem: React.FC<DetailItemProps> = ({
  label,
  value,

  highlight = false,
}) => {
  return (
    <div className={`p-3 rounded-lg border border-gray-200`}>
      <div className="flex justify-between items-start">
        <span className="text-sm font-medium  flex items-center">{label}</span>
        <span
          className={`text-base font-semibold ${
            highlight ? "text-blue-700" : ""
          }`}
        >
          {value}
        </span>
      </div>
    </div>
  );
};

export default DetailItem;
