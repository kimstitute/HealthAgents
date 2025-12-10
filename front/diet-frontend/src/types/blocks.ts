// 1. 블록 타입 종류
export type BlockType = 
  | 'markdown' 
  | 'chart' 
  | 'table' 
  | 'image' 
  | 'row'          
  | 'map'          
  | 'air_quality'; 

// 2. 공통 기본 인터페이스
export interface BaseBlock {
  id?: string; 
  type: BlockType;
}

// -------------------- [개별 블록 상세 정의] --------------------

export interface MarkdownBlock extends BaseBlock {
  type: 'markdown';
  content: string;
}

export interface ImageBlock extends BaseBlock {
  type: 'image';
  url: string;
  alt: string;
  caption?: string;
}

export interface ChartBlock extends BaseBlock {
  type: 'chart';
  chartType: 'bar' | 'line' | 'doughnut' | 'pie' | 'radar' | 'polarArea';
  title: string;
  description?: string;
  data: {
    labels: string[];
    values: number[];
  };
}

export interface TableBlock extends BaseBlock {
  type: 'table';
  title: string;
  description?: string;
  headers: string[];
  rows: string[][];
}

export interface MapBlock extends BaseBlock {
  type: 'map';
  title: string;
  description?: string;
  center: { lat: number; lng: number };
  zoom?: number;
  markers?: Array<{
    lat: number;
    lng: number;
    label?: string;
    type?: 'restaurant' | 'attraction' | 'transit' | 'facility';
  }>;
}

export interface AirQualityBlock extends BaseBlock {
  type: 'air_quality';
  title: string;
  aqi: number;
  status: 'good' | 'moderate' | 'unhealthy' | 'hazardous';
  description?: string;
}

// 3. 순환 참조를 위한 RowBlock 정의
// (Block 타입이 정의되기 전에 사용되므로, 여기서는 children 타입을 나중에 해석하도록 함)
export interface RowBlock extends BaseBlock {
  type: 'row';
  gap?: string; 
  children: Block[]; // 여기서 Block을 참조 (순환 참조)
}

// 4. 최종 유니온 타입 (메인 export)
export type Block = 
  | MarkdownBlock 
  | ImageBlock 
  | ChartBlock 
  | TableBlock 
  | RowBlock 
  | MapBlock 
  | AirQualityBlock;

