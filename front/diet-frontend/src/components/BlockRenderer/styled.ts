// src/components/BlockRenderer/styled.ts
import styled from 'styled-components';

export const BlockRenderContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* --- 1. Markdown --- */
  .markdown-block {
    font-size: 15px;
    line-height: 1.6;
    color: #2c3e50;
    
    h1, h2, h3 { margin: 12px 0 4px; font-weight: 700; color: #1a1a1a; }
    ul, ol { padding-left: 20px; margin-bottom: 8px; }
    strong { color: #007bff; }
    blockquote {
      border-left: 4px solid #ddd;
      padding-left: 12px;
      color: #666;
      background: #f8f9fa;
    }
  }

  /* --- 2. Chart --- */
  .chart-block {
    background: #fff;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1px solid #eee;

    .chart-block-title { font-size: 14px; font-weight: 600; text-align: center; margin-bottom: 12px; }
    .chart-block-container { position: relative; height: 250px; display: flex; justify-content: center; }
    .chart-block-description { margin-top: 12px; font-size: 12px; color: #888; text-align: center; }
  }

  /* --- 3. Image --- */
  .image-block {
    display: flex; flex-direction: column; align-items: center;
    img { width: 100%; max-width: 400px; border-radius: 12px; }
    .image-block-caption { margin-top: 8px; font-size: 12px; color: #888; }
  }

  /* --- 4. Table --- */
  .table-block {
    background: #fff; border-radius: 8px; padding: 12px; border: 1px solid #eee;
    
    .table-block-title { font-weight: 700; margin-bottom: 8px; font-size: 14px; }
    .table-wrapper { overflow-x: auto; }
    
    table {
      width: 100%; border-collapse: collapse; font-size: 13px; min-width: 300px;
      th { background: #f8f9fa; padding: 8px; text-align: left; border-bottom: 2px solid #eee; white-space: nowrap; }
      td { padding: 8px; border-bottom: 1px solid #f1f1f1; }
    }
  }

  /* --- 5. Map --- */
  .map-block {
    background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #eee;
    
    .map-title { padding: 10px 14px; background: #f8f9fa; font-weight: 600; font-size: 14px; margin: 0; }
    .map-container { height: 200px; background: #e9ecef; display: flex; align-items: center; justify-content: center; }
    .map-container img { width: 100%; height: 100%; object-fit: cover; }
    .map-placeholder { font-size: 12px; color: #888; text-align: center; }
    .map-description { padding: 10px; font-size: 12px; color: #666; }
  }

  /* --- 6. Row (Layout) --- */
  .row-block {
    display: flex; width: 100%;
    @media (max-width: 600px) { flex-direction: column !important; gap: 16px !important; }
  }

  /* --- 7. Air Quality --- */
  .air-quality-block {
    background: linear-gradient(135deg, #e3fdfd 0%, #ffe6fa 100%);
    border-radius: 16px; padding: 16px; text-align: center;
    
    .aqi-score { font-size: 32px; font-weight: 800; color: #20c997; margin: 4px 0; }
    .aqi-status { display: inline-block; background: rgba(255,255,255,0.7); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
  }
`;