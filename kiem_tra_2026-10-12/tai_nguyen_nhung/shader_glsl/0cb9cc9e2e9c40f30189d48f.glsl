
  uniform sampler2D uMaskMap;
  uniform sampler2D uArtMap;
  uniform sampler2D uCoatMap;
  uniform sampler2D uDepthMap;
  uniform float uUseDepthMap;
  uniform float uPreparation;
  uniform float uPreparationRelief;
  uniform float uDecorationRelief;
  uniform vec3 uTopColor;
  uniform vec3 uMidColor;
  uniform vec3 uAmberColor;
  uniform vec3 uGoldColor;
  uniform vec3 uEggshellColor;
  uniform float uRoughness;
  uniform float uPolishSplit;
  uniform float uMaterialDepth;
  uniform float uCompareBefore;
  uniform float uCoatSplit;
  uniform float uTime;
  uniform float uWaterDroplets;
  uniform float uCoatLayers;

  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vViewPosition;
  varying vec3 vWorldPosition;

  void main() {
    // Local sanding depth from dynamic mask (0.0 = pristine topcoat, 1.0 = fully sanded)
    float rawDepth = texture2D(uMaskMap, vUv).r * (1.0 - uCompareBefore);
    if (uPreparation > 0.5) rawDepth = 180.0 / 255.0;
    // The comparison side shows the artwork before coating; painting stays in the mask.
    float localMaterialDepth = mix(uMaterialDepth, texture2D(uDepthMap, vUv).r, uUseDepthMap);
    float sandDepth = clamp(rawDepth / (0.6 + localMaterialDepth * 0.8), 0.0, 1.0);
    vec4 artSample = texture2D(uArtMap, vUv);
    // Canvas coat masks store white RGB even for a faint translucent stroke. Read alpha,
    // otherwise one delicate pass is interpreted as a fully opaque, wide white glaze.
    float coatAmount = texture2D(uCoatMap, vUv).a * clamp(uCoatLayers / 2.0, 0.0, 1.0);
    // Keep the sanding mask identical on both sides of the finish comparison. Only the clear-film
    // reflection changes across the divider; pigment and inlay remain crisp and in place.
    if (vUv.x < 1.0 - uCoatSplit) coatAmount = 0.0;

    // Reveal the colored ground first, then composite only opaque artwork pixels.
    // Transparent pixels in a PNG must expose lacquer layers, never RGB black.
    vec3 upperLayer = mix(uTopColor, mix(uAmberColor, uMidColor, 0.4), smoothstep(0.0, 0.42, sandDepth));
    vec3 exposedGround = mix(mix(uAmberColor, uMidColor, 0.8), mix(uGoldColor, uEggshellColor, 0.28), smoothstep(0.34, 0.82, sandDepth));
    vec3 baseColor = mix(upperLayer, exposedGround, smoothstep(0.2, 0.55, sandDepth));
    float revealThreshold = 0.33 + localMaterialDepth * 0.28;
    float artReveal = artSample.a * smoothstep(revealThreshold, revealThreshold + 0.08, rawDepth);
    baseColor = mix(baseColor, artSample.rgb, artReveal);

    // Abrasion beyond the artwork reveals the ground and destroys fine detail locally.
    float worn = smoothstep(0.94, 1.0, rawDepth);
    float grain = fract(sin(dot(vUv, vec2(127.1, 311.7))) * 43758.5453);
    baseColor = mix(baseColor, vec3(0.17, 0.085, 0.035) + grain * 0.035, worn * 0.9);

    // PBR-inspired lighting calculation with Blinn-Phong specular & Fresnel clearcoat
    vec3 N = normalize(vNormal);
    if (uPreparation > 0.5) {
      vec2 texel = vec2(1.0 / 1536.0, 1.0 / 1024.0);
      float leftHeight = dot(texture2D(uArtMap, vUv - vec2(texel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));
      float rightHeight = dot(texture2D(uArtMap, vUv + vec2(texel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));
      float lowHeight = dot(texture2D(uArtMap, vUv - vec2(0.0, texel.y)).rgb, vec3(0.299, 0.587, 0.114));
      float highHeight = dot(texture2D(uArtMap, vUv + vec2(0.0, texel.y)).rgb, vec3(0.299, 0.587, 0.114));
      N = normalize(N + vec3(leftHeight - rightHeight, lowHeight - highHeight, 0.0) * uPreparationRelief * 35.0);
    }
    // User-painted material strokes live in the artwork map. Let their real texture luminance
    // create a restrained relief response so eggshell, gold leaf and mother-of-pearl read as
    // inlay under the clear lacquer, rather than flat colored decals.
    if (uDecorationRelief > 0.0) {
      vec2 artTexel = vec2(1.0 / 1536.0, 1.0 / 1024.0);
      float leftArt = dot(texture2D(uArtMap, vUv - vec2(artTexel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));
      float rightArt = dot(texture2D(uArtMap, vUv + vec2(artTexel.x, 0.0)).rgb, vec3(0.299, 0.587, 0.114));
      float lowArt = dot(texture2D(uArtMap, vUv - vec2(0.0, artTexel.y)).rgb, vec3(0.299, 0.587, 0.114));
      float highArt = dot(texture2D(uArtMap, vUv + vec2(0.0, artTexel.y)).rgb, vec3(0.299, 0.587, 0.114));
      N = normalize(N + vec3(leftArt - rightArt, lowArt - highArt, 0.0) * uDecorationRelief);
    }
    vec3 V = normalize(vViewPosition);
    vec3 L = normalize(vec3(1.8, 3.5, 2.2));
    vec3 frontL = normalize(vec3(0.2, 0.45, 1.0));
    vec3 H = normalize(mix(L, frontL, 0.48) + V);

    float NdotL = max(dot(N, L), 0.0);
    float NdotV = max(dot(N, V), 0.0);

    // Ambient + Diffuse
    vec3 ambient = vec3(0.15) * baseColor;
    float frontDiffuse = max(dot(N, frontL), 0.0);
    vec3 diffuse = (NdotL * 0.42 + frontDiffuse * 0.7) * baseColor;

    // Specular highlight: High clearcoat gloss characteristic of hand-polished lacquer
    float roughness = vUv.x <= uPolishSplit ? uRoughness : 0.85;
    float specExponent = mix(180.0, 12.0, clamp(roughness, 0.0, 1.0));
    float spec = pow(max(dot(N, H), 0.0), specExponent);

    // Fresnel rim reflection
    float fresnel = pow(1.0 - NdotV, 3.0) * 0.45;

    // Specular color tints toward gold where gold under-layer is exposed
    float goldPresence = smoothstep(0.5, 0.9, sandDepth) * artSample.a;
    vec3 specColor = mix(vec3(1.0, 0.98, 0.95), uGoldColor, goldPresence * 0.85);

    vec3 finalColor = ambient + diffuse + (spec * (1.0 - roughness * 0.85) + fresnel * (1.0 - roughness)) * specColor;

    // Clear lacquer adds a crisp, neutral reflection. Keep pigment, inlay, and artwork pixels untouched:
    // a transparent coat must not tint, darken, blur, or replace the decoration beneath it.
    float coatResponse = clamp(uCoatLayers / 2.0, 0.0, 1.0);
    float clearFilm = coatAmount * (0.72 + coatResponse * 0.28);
    // A broad low-exponent lobe reads as a white veil and washes out inlay detail.
    // Keep the clear film neutral and visible only as a restrained, tight highlight.
    float coatReflection = pow(max(dot(N, H), 0.0), mix(110.0, 180.0, coatResponse));
    float edgeReflection = pow(1.0 - NdotV, 5.0);
    finalColor += vec3(1.0, 0.98, 0.93) * clearFilm * (coatReflection * 0.2 + edgeReflection * 0.045);

    // Micro-ripple wet water sheen when freshly abraded
    if (sandDepth > 0.03 && uWaterDroplets > 0.0) {
      float ripple = sin(vUv.x * 50.0 + uTime * 4.0) * cos(vUv.y * 50.0 + uTime * 3.0);
      float waterGlint = max(0.0, ripple) * 0.12 * uWaterDroplets * sandDepth;
      finalColor += vec3(waterGlint * 0.8, waterGlint * 0.9, waterGlint);
    }

    gl_FragColor = vec4(finalColor, 1.0);
    if (uPreparation > 0.5) gl_FragColor.rgb = pow(max(finalColor, vec3(0.0)), vec3(1.0 / 2.2));
  }
