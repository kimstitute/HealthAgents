// src/styled.d.ts
import "styled-components";
import type { AppTheme } from "./theme";  // theme.ts 위치에 맞게 경로 조정!

declare module "styled-components" {
  // 여기서 DefaultTheme를 우리 AppTheme으로 확장
  export interface DefaultTheme extends AppTheme {}
}

