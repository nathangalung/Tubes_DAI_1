'use client'

import { useEffect, useRef } from 'react'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function SteepestAscentVisualization() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (canvasRef.current) {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      if (ctx) {
        const resizeObserver = new ResizeObserver(() => {
          resizeCanvas(canvas, ctx)
        })
        resizeObserver.observe(canvas)
        return () => resizeObserver.disconnect()
      }
    }
  }, [])

  const resizeCanvas = (canvas: HTMLCanvasElement, ctx: CanvasRenderingContext2D) => {
    const container = canvas.parentElement
    if (container) {
      canvas.width = container.clientWidth
      canvas.height = 300
      drawChart(ctx)
    }
  }

  const drawChart = (ctx: CanvasRenderingContext2D) => {
    const width = ctx.canvas.width
    const height = ctx.canvas.height

    // Clear canvas
    ctx.clearRect(0, 0, width, height)

    // Draw grid
    ctx.strokeStyle = '#2d364d'
    ctx.lineWidth = 1

    // Vertical grid lines
    for (let i = 0; i < width; i += 40) {
      ctx.beginPath()
      ctx.moveTo(i, 0)
      ctx.lineTo(i, height)
      ctx.stroke()
    }

    // Horizontal grid lines
    for (let i = 0; i < height; i += 40) {
      ctx.beginPath()
      ctx.moveTo(0, i)
      ctx.lineTo(width, i)
      ctx.stroke()
    }

    // Draw fitness curve
    ctx.strokeStyle = '#4f46e5'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(0, height)

    // Create a curve that starts high and decreases
    for (let x = 0; x < width; x++) {
      const progress = x / width
      const y = height * (0.2 + Math.exp(-progress * 3) * 0.6)
      ctx.lineTo(x, y)
    }
    ctx.stroke()

    // Draw average fitness curve
    ctx.strokeStyle = '#22c55e'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(0, height * 0.8)

    for (let x = 0; x < width; x++) {
      const progress = x / width
      const y = height * (0.3 + Math.exp(-progress * 2.5) * 0.4)
      ctx.lineTo(x, y)
    }
    ctx.stroke()
  }

  return (
    <div className="bg-[#0a0a0a] text-white font-['Space_Grotesk',system-ui,sans-serif] min-h-screen p-8">
      <div className="max-w-[1400px] mx-auto">
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#111318] rounded-lg text-[#94a3b8] hover:text-white transition-colors mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </Link>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-[#111318] rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-[#4f46e5]" />
              <h2 className="text-lg font-semibold">Initial State</h2>
            </div>
            <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-4" />
            <div className="text-sm text-[#94a3b8]">Initial State Objective Function: 6505</div>
          </div>
          <div className="bg-[#111318] rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-[#22c55e]" />
              <h2 className="text-lg font-semibold">Final State</h2>
            </div>
            <div className="w-full aspect-video bg-[#1a1d24] rounded-lg mb-4" />
            <div className="text-sm text-[#94a3b8]">Final State Objective Function: 104</div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          {[
            { title: 'Solution Cost', value: '104' },
            { title: 'Time Elapsed', value: '18.76s' },
            { title: 'Number of Iterations', value: '1500' },
          ].map((metric, index) => (
            <div key={index} className="bg-[#111318] rounded-2xl p-6">
              <h3 className="text-sm text-[#94a3b8] mb-2">{metric.title}</h3>
              <div className="text-2xl font-bold text-[#4f46e5]">{metric.value}</div>
            </div>
          ))}
        </div>

        <div className="bg-[#111318] rounded-2xl p-6">
          <h3 className="mb-4">Plot of Fitness Values vs Iteration</h3>
          <canvas ref={canvasRef} className="w-full h-[300px] bg-[#1a1d24] rounded-lg" />
        </div>
      </div>
    </div>
  )
}