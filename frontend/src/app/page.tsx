"use client";

import { PointMaterial, Points } from "@react-three/drei";
import { Canvas, useFrame } from "@react-three/fiber";
import { inSphere } from "maath/random";
import { useRef, useState } from "react";

export default function Page() {
	return (
		<main className="h-screen w-screen bg-black">
			<Hero />
			<Canvas camera={{ position: [0, 0, 1] }}>
				<Stars />
			</Canvas>
		</main>
	);
}

function Stars() {
	const ref = useRef<THREE.Points>(null);
	const [sphere] = useState(
		() => inSphere(new Float32Array(5000), { radius: 1.5 }) as Float32Array
	);
	useFrame((state, delta) => {
		if (!ref.current) return;
		ref.current.rotation.x -= delta / 10;
		ref.current.rotation.y -= delta / 15;
	});
	return (
		<group rotation={[0, 0, Math.PI / 4]}>
			<Points frustumCulled={false} positions={sphere} ref={ref} stride={3}>
				<PointMaterial
					color="#ffa0e0"
					depthWrite={false}
					size={0.005}
					sizeAttenuation={true}
					transparent
				/>
			</Points>
		</group>
	);
}

function Hero() {
	return (
		<div className="fixed left-0 top-0 z-10 flex h-screen w-screen flex-col items-center justify-center text-white">
			<AiFace />

			<div className="pointer-events-none mt-[-100px] text-4xl font-bold sm:text-5xl md:text-6xl lg:text-8xl">
				OpenAgent
			</div>

			<Input />

			<div className="pointer-events-none mt-5 text-3xl">
				AI that <span className="text-red-500">executes</span>.
			</div>

			{/* <div className="pointer-events-none mt-5 text-gray-200">Coming soon.</div> */}
			<Button
				component={Link}
				gradient={{
					deg: 45,
					from: "red",
					to: "pink",
				}}
				href="/app"
				my="md"
				size="lg"
				variant="gradient"
			>
				START FREE TRIAL
			</Button>
		</div>
	);
}

import { useRive } from "@rive-app/react-canvas";

function AiFace() {
	const { RiveComponent } = useRive({
		autoplay: true,
		src: "/assets/rive/ai-face.riv",
		stateMachines: "State Machine 1",
	});

	return (
		<div className="mt-[-150px] h-[400px] w-full">
			<RiveComponent />
		</div>
	);
}

import { ActionIcon, Button } from "@mantine/core";
import { showNotification } from "@mantine/notifications";
import { IconRobot } from "@tabler/icons-react";
import Link from "next/link";
import Typewriter from "typewriter-effect";

function Input() {
	return (
		// mocked input
		<div className="mt-10 flex h-[50px] w-[600px] max-w-[95%] items-center justify-between rounded-lg bg-gray-800 p-5">
			<Typewriter
				options={{
					autoStart: true,
					delay: 50,
					deleteSpeed: 5,
					loop: true,
					strings: [
						"A personalized AI assistant to help you accomplish more!",
						"Empowering your digital journey with AI assistance.",
						"Unleash your productivity with OpenAgent's AI guidance.",
						"Simplify and supercharge your tasks with OpenAgent AI.",
						"Elevate your efficiency with OpenAgent's personalized AI support.",
						"Unlock your potential with OpenAgent's intelligent assistance.",
						"Navigate the digital realm effortlessly with OpenAgent AI.",
						"Your trusted AI companion for seamless productivity.",
						"Maximize your capabilities with OpenAgent's smart guidance.",
						"Accelerate your success with OpenAgent's AI-driven support.",
						"Seize control of your digital experience with OpenAgent AI.",
					],
				}}
			/>

			<ActionIcon
				color="red"
				onClick={() => {
					showNotification({
						color: "red",
						message: "OpenAgent is still in development.",
						title: "Coming soon!",
					});
				}}
				variant="light"
			>
				<IconRobot />
			</ActionIcon>
		</div>
	);
}
