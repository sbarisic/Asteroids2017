uniform sampler2D tex;

uniform float color_mul;
uniform float pixelate;
uniform float time;
uniform float width;
uniform float height;

uniform vec2 chroma_r;
uniform vec2 chroma_g;
uniform vec2 chroma_b;

const float NoiseScale = 0.1;
const float Disortion = 0.3;
const float Rescale = 1.0 - (0.25 * Disortion);
const vec3 BorderColor = vec3(0, 0, 0);

// https://github.com/mattdesl/glsl-random Magic :D
float rnd(vec2 co) { return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453); }

vec4 tex2d(sampler2D texture, vec2 coords) {
	/*float d = 1.0 / pixelate;
	float u = floor(coords.x / d) * d;
	d = (width / height) / pixelate;
	float v = floor(coords.y / d) * d;
	return texture2D(texture, vec2(u, v));*/

	return texture2D(texture, coords);
}

void main() {
	vec2 TexCoord = gl_TexCoord[0].xy - vec2(0.5);
	TexCoord = ((TexCoord + (TexCoord * (Disortion * (TexCoord.x * TexCoord.x + TexCoord.y * TexCoord.y)))) * Rescale) + vec2(0.5);

	float ColorMul = 1.0 - float(abs(TexCoord.x - 0.5) > 0.5 || abs(TexCoord.y - 0.5) > 0.5);

	vec2 sz = vec2(width, height);
	vec2 ro = chroma_r / sz;
	vec2 go = chroma_g / sz;
	vec2 bo = chroma_b / sz;

	float R = tex2d(tex, TexCoord + ro).r + rnd(TexCoord + vec2(time, time)) * NoiseScale;
	float G = tex2d(tex, TexCoord + go).g + rnd(TexCoord + vec2(time, -time)) * NoiseScale;
	float B = tex2d(tex, TexCoord + bo).b + rnd(TexCoord + vec2(-time, -time)) * NoiseScale;

	vec3 screen_clr = abs(vec3(R, G, B) - color_mul);
	gl_FragColor = vec4(mix(BorderColor, screen_clr, ColorMul), 1.0) * gl_Color;
}