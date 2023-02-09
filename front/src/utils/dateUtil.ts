/**
 * Independent time operation tool to facilitate subsequent switch to dayjs
 */
import dayjs from 'dayjs';

const DATE_TIME_FORMAT = 'YYYY-MM-DD HH:mm:ss';
const DATE_FORMAT = 'YYYY-MM-DD';

export function formatToDateTime(
  date: dayjs.Dayjs | undefined = undefined,
  format = DATE_TIME_FORMAT,
): string {
  return dayjs(date).format(format);
}

export function formatToDate(
  date: dayjs.Dayjs | undefined = undefined,
  format = DATE_FORMAT,
): string {
  return dayjs(date).format(format);
}

export function timestampToDate(timestamp: number): string {
  // 时间戳（精确到秒，10位）转为'xx年xx月xx日'
  const date = new Date(timestamp * 1000);
  const year = date.getFullYear();
  const month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
  const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
  const hour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours();
  const minute = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
  const second = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();
  const str = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
  return str;
}

export function timestampToDate1(timestamp: number): string {
  // GMT时间戳（精确到秒，10位）转为'2022-12-05 16:00:01'北京时间
  const date = new Date((timestamp + 28800) * 1000);
  const year = date.getFullYear();
  const month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
  const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
  const hour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours();
  const minute = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
  const second = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();
  const str = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
  return str;
}

export const dateUtil = dayjs;
