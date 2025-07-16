interface NavProps {
  expand: boolean;
  text: string;
  image: string;
  onClick?: () => void;
}
const NavItem: React.FC<NavProps> = ({ expand, text, image, onClick }) => {
  return (
    <>
      <div
        className="flex align-center items-center hover:bg-gray-500/20 rounded-lg transition-all duration-300 cursor-pointer"
        onClick={onClick}
      >
        <div className="group relative flex items-center justify-center h-9 w-9 aspect-square rounded-lg">
          <img
            src={image}
            width={20}
            height={20}
            alt="New task"
            className="dark:invert"
          />
        </div>
        <p
          className={`overflow-hidden whitespace-nowrap transition-all duration-300 ${
            expand ? "opacity-100 w-auto ml-2" : "opacity-0 w-0"
          }`}
        >
          {text}
        </p>
      </div>
    </>
  );
};
export default NavItem;
