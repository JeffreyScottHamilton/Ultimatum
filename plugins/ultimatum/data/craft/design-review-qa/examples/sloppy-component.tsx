import { Rocket } from "lucide-react";
import { FaStar } from "react-icons/fa";

export default function Hero({ open }: { open: boolean }) {
  return (
    <section className={cn("hero min-h-screen bg-gradient-to-r from-purple-600 to-indigo-500", open && "w-screen")}>
      <span className="rounded-full px-3 py-1 uppercase tracking-widest text-[10px]">Beta</span>
      <h1 className="text-9xl italic uppercase leading-none bg-clip-text text-transparent bg-gradient-to-r from-violet-500 to-pink-500">
        Build faster
      </h1>
      <button className="h-16 transition-all animate-bounce outline-none rounded-xl">Get started</button>
      <span className="animate-ping h-2 w-2 rounded-full bg-green-500" />
      <div className="sticky top-0"><Rocket /></div>
      <div className="sticky top-0"><FaStar /></div>
    </section>
  );
}
