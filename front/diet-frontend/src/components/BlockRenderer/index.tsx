// src/components/BlockRenderer/index.tsx
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  Chart as ChartJS, ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale, BarElement, PointElement, LineElement, RadialLinearScale
} from 'chart.js';
import { Doughnut, Bar, Line, Pie, Radar, PolarArea } from 'react-chartjs-2';

// 위에서 만든 타입 가져오기
import type { Block as BlockType } from '../../types/blocks';
// 스타일 가져오기
import * as S from './styled'; 

// ChartJS 플러그인 등록 (필수)
ChartJS.register(
  ArcElement, Tooltip, Legend, CategoryScale, LinearScale, 
  BarElement, PointElement, LineElement, RadialLinearScale
);

const COLORS = [
  'rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 'rgba(255, 206, 86, 0.8)',
  'rgba(75, 192, 192, 0.8)', 'rgba(153, 102, 255, 0.8)', 'rgba(255, 159, 64, 0.8)'
];

/* -------------------- [하위 컴포넌트들] -------------------- */

const MarkdownComponent = ({ block }: { block: BlockType & { type: 'markdown' } }) => (
  <div className="markdown-block">
    <ReactMarkdown>{block.content}</ReactMarkdown>
  </div>
);

const ImageComponent = ({ block }: { block: BlockType & { type: 'image' } }) => (
  <div className="image-block">
    <img src={block.url} alt={block.alt} />
    {block.caption && <p className="image-block-caption">{block.caption}</p>}
  </div>
);

const ChartComponent = ({ block }: { block: BlockType & { type: 'chart' } }) => {
  const chartData = {
    labels: block.data.labels,
    datasets: [{
      label: block.title,
      data: block.data.values,
      backgroundColor: COLORS.slice(0, block.data.labels.length),
      borderWidth: 1,
    }],
  };
  const options = { responsive: true, plugins: { legend: { position: 'bottom' as const } } };

  const renderChart = () => {
    switch (block.chartType) {
      case 'doughnut': return <Doughnut data={chartData} options={options} />;
      case 'pie': return <Pie data={chartData} options={options} />;
      case 'line': return <Line data={chartData} options={options} />;
      case 'radar': return <Radar data={chartData} options={options} />;
      default: return <Bar data={chartData} options={options} />;
    }
  };

  return (
    <div className="chart-block">
      <h4 className="chart-block-title">{block.title}</h4>
      <div className="chart-block-container">{renderChart()}</div>
      {block.description && <p className="chart-block-description">{block.description}</p>}
    </div>
  );
};

const TableComponent = ({ block }: { block: BlockType & { type: 'table' } }) => (
  <div className="table-block">
    <h4 className="table-block-title">{block.title}</h4>
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>{block.headers.map((h, i) => <th key={i}>{h}</th>)}</tr>
        </thead>
        <tbody>
          {block.rows.map((row, i) => (
            <tr key={i}>{row.map((c, j) => <td key={j}>{c}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

const MapComponent = ({ block }: { block: BlockType & { type: 'map' } }) => {
  const [error, setError] = useState(false);
  const apiKey = (import.meta as any).env.VITE_GOOGLE_MAPS_API_KEY || '';
  
  const staticMapUrl = apiKey 
    ? `https://maps.googleapis.com/maps/api/staticmap?center=${block.center.lat},${block.center.lng}&zoom=${block.zoom||15}&size=600x400&markers=color:red|${block.center.lat},${block.center.lng}&key=${apiKey}`
    : ''; 

  return (
    <div className="map-block">
      <h3 className="map-title">{block.title}</h3>
      <div className="map-container">
        {staticMapUrl && !error ? (
          <img src={staticMapUrl} alt="map" onError={() => setError(true)} />
        ) : (
          <div className="map-placeholder">
            <div>🗺️ 지도 ({block.center.lat.toFixed(3)}, {block.center.lng.toFixed(3)})</div>
          </div>
        )}
      </div>
      {block.description && <p className="map-description">{block.description}</p>}
    </div>
  );
};

const AirQualityComponent = ({ block }: { block: BlockType & { type: 'air_quality' } }) => (
  <div className="air-quality-block">
    <h4>{block.title}</h4>
    <div className="aqi-score">{block.aqi}</div>
    <div className="aqi-status">{block.status.toUpperCase()}</div>
  </div>
);

// RowBlock (재귀 호출을 위해 아래 Block을 사용)
const RowComponent = ({ block }: { block: BlockType & { type: 'row' } }) => (
  <div className="row-block" style={{ gap: block.gap || '16px' }}>
    {block.children.map((child, i) => (
      <div key={i} style={{ flex: 1 }}> 
        <Block block={child} /> 
      </div>
    ))}
  </div>
);

/* -------------------- [메인 내보내기] -------------------- */
export const Block = ({ block }: { block: BlockType }) => {
  if (!block) return null;

  switch (block.type) {
    case 'markdown':    return <MarkdownComponent block={block} />;
    case 'image':       return <ImageComponent block={block} />;
    case 'chart':       return <ChartComponent block={block} />;
    case 'table':       return <TableComponent block={block} />;
    case 'map':         return <MapComponent block={block} />;
    case 'air_quality': return <AirQualityComponent block={block} />;
    case 'row':         return <RowComponent block={block} />;
    default:            return null;
  }
};