"""
MediGuard 医保智盾 — AI驱动的医保合规和风控引擎

用户视角：上传医保报销数据 → AI自动审核 → 找出违规项 → 降低拒付率
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    CRITICAL = "极高风险"


@dataclass
class AuditResult:
    """审核结果"""
    claim_id: str
    risk_level: str
    violations: List[str]
    suggestions: List[str]
    potential_savings: float
    confidence: float


class ComplianceEngine:
    """医保合规审核引擎"""
    
    # 常见违规规则
    RULES = {
        "超量开药": {
            "desc": "单次处方超过规定用量",
            "severity": RiskLevel.HIGH,
            "penalty_rate": 1.0,
        },
        "过度检查": {
            "desc": "无适应症的检查项目",
            "severity": RiskLevel.MEDIUM,
            "penalty_rate": 0.8,
        },
        "串换药品": {
            "desc": "用低价药串换为高价药报销",
            "severity": RiskLevel.CRITICAL,
            "penalty_rate": 2.0,
        },
        "分解收费": {
            "desc": "将一个服务拆分为多个项目收费",
            "severity": RiskLevel.HIGH,
            "penalty_rate": 1.5,
        },
        "重复收费": {
            "desc": "对同一服务重复收费",
            "severity": RiskLevel.HIGH,
            "penalty_rate": 1.0,
        },
    }
    
    def audit_claims(self, claims: List[Dict]) -> List[AuditResult]:
        """批量审核报销单"""
        results = []
        for claim in claims:
            result = self._audit_single(claim)
            results.append(result)
        return results
    
    def _audit_single(self, claim: Dict) -> AuditResult:
        """单个报销单审核"""
        violations = []
        suggestions = []
        potential_savings = 0.0
        
        claim_id = claim.get("id", "unknown")
        amount = claim.get("amount", 0)
        items = claim.get("items", [])
        
        # 规则检查
        for item in items:
            name = item.get("name", "")
            qty = item.get("quantity", 1)
            price = item.get("price", 0)
            
            # 超量检查
            if qty > 10:  # 简化规则
                violations.append(f"超量开药: {name} (数量{qty})")
                potential_savings += price * (qty - 5)
            
            # 价格异常
            if price > 5000:
                suggestions.append(f"高价项目需审核: {name} (¥{price})")
        
        # 计算风险等级
        if len(violations) > 3:
            risk = RiskLevel.CRITICAL.value
        elif len(violations) > 1:
            risk = RiskLevel.HIGH.value
        elif violations:
            risk = RiskLevel.MEDIUM.value
        else:
            risk = RiskLevel.LOW.value
        
        return AuditResult(
            claim_id=claim_id,
            risk_level=risk,
            violations=violations,
            suggestions=suggestions,
            potential_savings=potential_savings,
            confidence=0.85
        )
    
    def generate_report(self, results: List[AuditResult]) -> str:
        """生成审核报告"""
        total = len(results)
        violations_count = sum(len(r.violations) for r in results)
        total_savings = sum(r.potential_savings for r in results)
        
        lines = [
            "📊 医保合规审核报告",
            f"",
            f"审核报销单: {total} 份",
            f"发现违规: {violations_count} 项",
            f"潜在节省: ¥{total_savings:,.0f}",
            "",
            "=== 高风险项目 ===",
        ]
        
        for r in results:
            if r.risk_level in [RiskLevel.HIGH.value, RiskLevel.CRITICAL.value]:
                lines.append(f"  🔴 {r.claim_id}: {', '.join(r.violations[:2])}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    engine = ComplianceEngine()
    test_claims = [
        {"id": "CLM-001", "amount": 15000, "items": [
            {"name": "头孢克肟", "quantity": 15, "price": 200},
            {"name": "CT检查", "quantity": 1, "price": 800},
        ]},
    ]
    results = engine.audit_claims(test_claims)
    print(engine.generate_report(results))
