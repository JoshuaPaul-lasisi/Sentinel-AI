import { Nav } from "@ui/molecules/Nav";
import Link from "next/link";
import { IconType } from "react-icons/lib";
import { VscGraphLine } from "react-icons/vsc";
import { GrTransaction } from "react-icons/gr";
import { PiDetectiveDuotone } from "react-icons/pi";
import Image from "next/image";
export default function Home() {
  return (
    <div className="relative">
      <Nav />
      <div className="absolute top-0 left-0 w-72 h-72 bg-primary-100 rounded-full blur-3xl opacity-50"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-red-100 rounded-full blur-3xl opacity-50"></div>
      <div className="absolute top-0 right-0 w-96 h-96 bg-red-200 rounded-full blur-3xl opacity-50 "></div>

      <div className="min-h-screen bg-transparent font-nunito relative z-10">
        <div className="container mx-auto px-4 py-20">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 ">
              Sentinel <span className="text-primary-500">AI</span>
            </h1>

            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto tracking-wide mt-10">
              Africa-first fraud detection platform powered by behavioral
              anomaly detection and graph intelligence
            </p>
            <div className="space-y-4 mt-10">
              <div className="bg-white rounded-xl shadow-lg p-6 py-12 max-w-4xl mx-auto flex flex-col items-center ">
                <Image
                  src="/images/illustrations/vault.svg"
                  alt="Fraud Detection Illustration"
                  width={80}
                  height={80}
                  className="w-[300px] md:w-[400px] h-auto mb-8"
                />
                <h2 className="text-2xl font-semibold text-gray-800 mb-4 tracking-wide">
                  ₦52.26B Lost to Fraud in 2024
                </h2>
                <p className="text-gray-600 mb-4 tracking-wide ">
                  196% increase year-over-year • Nigerian banks absorb ₦1.5–2.2B
                  in uninsurable fraud costs annually
                </p>
              </div>
            </div>
            <Link
              href="/dashboard"
              className="inline-block mt-8 font-nunito bg-primary-500 text-white px-8 py-3 rounded-xl font-semibold hover:bg-primary-700 transition-colors"
            >
              Enter Dashboard
            </Link>
          </div>

          {/* Key Features */}
          <div className="mt-16 grid md:grid-cols-3 grid-cols-1 gap-8 md:gap-10 max-w-6xl mx-auto ">
            <KeyFeatures
              label="Real-time Transaction Monitoring"
              text="Instantly detects and flags suspicious activities"
              Icon={GrTransaction}
            />
            <KeyFeatures
              label="Behavioral Anomaly Detection"
              text="Learns each customer's transaction habits"
              Icon={PiDetectiveDuotone}
            />
            <KeyFeatures
              label="Graph Intelligence"
              text="Uncovers coordinated fraud networks"
              Icon={VscGraphLine}
            />
            {/* <KeyFeatures
            label="Explainable AI"
            text="Transparency and regulatory compliance"
          /> */}
          </div>
        </div>
      </div>
    </div>
  );
}

const KeyFeatures = ({
  label,
  text,
  Icon,
}: {
  label: string;
  text: string;
  Icon: IconType;
}) => {
  return (
    <div className="bg-white p-6 py-8 rounded-lg shadow-lg">
      <Icon className="text-red-700 text-5xl mb-4" />
      <h3 className="font-semibold text-lg mb-2">{label}</h3>
      <p className="text-gray-600">{text}</p>
    </div>
  );
};
