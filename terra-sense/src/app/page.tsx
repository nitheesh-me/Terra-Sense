import Image from "next/image";
import { Boxes } from "@/components/ui/background-boxes";

export default function Home() {
  return (
    <>
    <Boxes />
    {/* <GoogleEffect pathLengths={[]} /> */}
    <div className="z-10 grid grid-rows-[20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] scroll-none">
      <main className="z-10 flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div className="center">
          <h1 className="text-xl sm:text-5xl font-bold text-center sm:text-left">
            Welcome to{" "}
            <span className="font-[family-name:var(--font-geist-mono)] text-primary">Terra Sense</span>
          </h1>
          <p className="text-center sm:text-left">
            Aim to provide a platform to monitor and predict natural disasters.
          </p>
        {/* <Image
          src="/hero.png"
          alt="Terra Sense"
          width={600}
          height={300}
          className="rounded-lg"
        /> */}
        </div>
      </main>
    </div>
    </>
  );
}
